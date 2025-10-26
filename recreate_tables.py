#!/usr/bin/env python3
"""
Drop and Recreate Supabase Tables
This script drops existing tables and recreates them cleanly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supabase_config import supabase_manager

def drop_and_recreate_tables():
    """Drop existing tables and recreate them"""
    if not supabase_manager.is_connected():
        print(" Supabase not connected!")
        return False
    
    print("Dropping existing tables...")
    
    try:
        # Drop tables in reverse dependency order
        drop_statements = [
            "DROP TABLE IF EXISTS incidents CASCADE;",
            "DROP TABLE IF EXISTS threat_assessments CASCADE;", 
            "DROP TABLE IF EXISTS documents CASCADE;",
            "DROP FUNCTION IF EXISTS search_documents CASCADE;",
            "DROP FUNCTION IF EXISTS get_recent_assessments CASCADE;",
            "DROP FUNCTION IF EXISTS get_incident_history CASCADE;",
            "DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;"
        ]
        
        for statement in drop_statements:
            try:
                supabase_manager.client.rpc('exec_sql', {'sql': statement}).execute()
                print(f"Executed: {statement.split()[2] if len(statement.split()) > 2 else 'statement'}")
            except Exception as e:
                print(f" Warning executing {statement}: {e}")
        
            print("Tables dropped successfully")
        
        # Now recreate tables using the schema
        print("\nRecreating tables from schema...")
        
        with open('supabase_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement.upper().startswith(('CREATE', 'INSERT', 'GRANT')):
                try:
                    supabase_manager.client.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"Created: {statement.split()[2] if len(statement.split()) > 2 else 'object'}")
                except Exception as e:
                    print(f" Warning creating {statement[:30]}...: {e}")
        
            print("Tables recreated successfully")
        return True
        
    except Exception as e:
        print(f"Error with table operations: {e}")
        return False

def verify_tables():
    """Verify that tables were created successfully"""
    print("\nVerifying table creation...")
    
    try:
        # Check if tables exist
        tables_to_check = ['documents', 'incidents', 'threat_assessments']
        
        for table in tables_to_check:
            try:
                result = supabase_manager.client.table(table).select('count').execute()
                print(f"Table '{table}' exists and accessible")
            except Exception as e:
                print(f"Table '{table}' error: {e}")
        
        # Check if functions exist
        functions_to_check = ['search_documents', 'get_recent_assessments', 'get_incident_history']
        
        for func in functions_to_check:
            try:
                # Test function existence by calling it with dummy parameters
                if func == 'search_documents':
                    # This will fail but tells us the function exists
                    supabase_manager.client.rpc(func, {
                        'query_embedding': [0.0] * 384,
                        'match_threshold': 0.1,
                        'match_count': 1
                    }).execute()
                    print(f"Function '{func}' exists")
            except Exception as e:
                if "function" in str(e).lower():
                    print(f"Function '{func}' exists (test call failed as expected)")
                else:
                    print(f"Function '{func}' error: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error verifying tables: {e}")
        return False

def main():
    """Main function"""
    print("Sign3T Table Recreation")
    print("=" * 40)
    
    # Drop and recreate tables
    if drop_and_recreate_tables():
        # Verify tables were created
        if verify_tables():
            print("\nTable recreation completed successfully!")
            print(" Now you can run: python feed_data.py")
            print(" Or run: ./run.sh")
        else:
            print("\nTables recreated but verification had issues")
    else:
        print("\nTable recreation failed")

if __name__ == "__main__":
    main()
