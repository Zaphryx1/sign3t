#!/usr/bin/env python3
"""
Properly Drop and Recreate Supabase Tables
This script uses direct Supabase operations to drop and recreate tables
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supabase_config import supabase_manager

def clear_all_data():
    """Clear all data from existing tables"""
    if not supabase_manager.is_connected():
        print(" Supabase not connected!")
        return False
    
    print("Clearing all data from existing tables...")
    
    try:
        # Clear incidents table using date filter (more effective)
        result = supabase_manager.client.table("incidents").delete().gte("created_at", "1900-01-01").execute()
        print(f"Cleared incidents table: {len(result.data) if result.data else 0} records")
        
        # Clear documents table using date filter
        result = supabase_manager.client.table("documents").delete().gte("created_at", "1900-01-01").execute()
        print(f"Cleared documents table: {len(result.data) if result.data else 0} records")
        
        # Clear threat assessments table using date filter
        result = supabase_manager.client.table("threat_assessments").delete().gte("created_at", "1900-01-01").execute()
        print(f"Cleared threat assessments table: {len(result.data) if result.data else 0} records")
        
        print("All data cleared successfully")
        return True
        
    except Exception as e:
        print(f"Error clearing data: {e}")
        return False

def verify_clean_tables():
    """Verify that tables are clean"""
    print("\nVerifying clean tables...")
    
    try:
        # Check incidents count
        incidents_result = supabase_manager.client.table("incidents").select("count").execute()
        incidents_count = len(incidents_result.data)
        print(f"Incidents table: {incidents_count} records")
        
        # Check documents count
        docs_result = supabase_manager.client.table("documents").select("count").execute()
        docs_count = len(docs_result.data)
        print(f"Documents table: {docs_count} records")
        
        # Check threat assessments count
        assessments_result = supabase_manager.client.table("threat_assessments").select("count").execute()
        assessments_count = len(assessments_result.data)
        print(f"Threat assessments table: {assessments_count} records")
        
        if incidents_count == 0 and docs_count == 0 and assessments_count == 0:
            print("All tables are clean!")
            return True
        else:
            print("Some tables still contain data")
            return False
        
    except Exception as e:
        print(f"Error verifying tables: {e}")
        return False

def main():
    """Main function"""
    print("Sign3T Clean Data Preparation")
    print("=" * 40)
    
    # Clear all data
    if clear_all_data():
        # Verify tables are clean
        if verify_clean_tables():
            print("\nData clearing completed successfully!")
            print(" Now you can run: python feed_data.py")
            print(" Or run: ./run.sh")
        else:
            print("\nData cleared but verification had issues")
    else:
        print("\nData clearing failed")

if __name__ == "__main__":
    main()
