#!/usr/bin/env python3
"""
Clear and Re-feed Supabase Data
This script clears existing data and re-feeds it cleanly to avoid duplicates
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supabase_config import supabase_manager

def clear_existing_data():
    """Clear existing data from Supabase tables"""
    if not supabase_manager.is_connected():
        print("Supabase not connected!")
        return False
    
    print("Clearing existing data...")
    
    try:
        # Clear incidents table
        supabase_manager.client.table("incidents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Cleared incidents table")
        
        # Clear documents table
        supabase_manager.client.table("documents").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Cleared documents table")
        
        # Clear threat assessments table
        supabase_manager.client.table("threat_assessments").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Cleared threat assessments table")
        
        return True
        
    except Exception as e:
        print(f"Warning: Error clearing data: {e}")
        return False

def main():
    """Main function"""
    print("Sign3T Data Cleanup and Re-feed")
    print("=" * 40)
    
    # Clear existing data
    if clear_existing_data():
        print("\nData cleared successfully!")
        print("Now you can run: python feed_data.py")
        print("Or run: ./run.sh")
    else:
        print("\nData cleanup failed.")

if __name__ == "__main__":
    main()
