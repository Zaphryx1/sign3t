#!/usr/bin/env python3
"""
Quick Setup Script for Sign3T Automated Supabase Integration
This script helps you set up automated table creation and data feeding
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print(" Checking requirements...")
    
    # Check if data files exist
    data_files = [
        'data/dispatch_records.json',
        'data/gis_data.json', 
        'data/prior_incidents.json',
        'data/sample_transcripts.json'
    ]
    
    missing_files = []
    for file in data_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f" Missing data files: {missing_files}")
        return False
    
    print(" All data files found")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print(" .env file not found")
        print("Please create a .env file with your Supabase credentials:")
        print("SUPABASE_URL=your_supabase_url")
        print("SUPABASE_ANON_KEY=your_anon_key")
        print("SUPABASE_SERVICE_ROLE_KEY=your_service_role_key")
        return False
    
    print(" .env file found")
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print(" Virtual environment not found")
        print("Please run: python3 -m venv venv")
        return False
    
    print(" Virtual environment found")
    
    return True

def setup_supabase_tables():
    """Set up Supabase tables using the schema"""
    print("\n Setting up Supabase tables...")
    
    try:
        # Import after checking requirements
        sys.path.insert(0, 'src')
        from supabase_config import supabase_manager
        
        if not supabase_manager.is_connected():
            print(" Cannot connect to Supabase")
            print("Please check your .env file and Supabase credentials")
            return False
        
        print(" Connected to Supabase")
        
        # Read and execute the schema
        with open('supabase_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        print(" Schema file loaded")
        print(" Please run the SQL schema in your Supabase dashboard:")
        print("   1. Go to your Supabase project dashboard")
        print("   2. Navigate to SQL Editor")
        print("   3. Copy the content from supabase_schema.sql")
        print("   4. Paste and run the SQL")
        print("   5. Make sure pgvector extension is enabled")
        
        return True
        
    except Exception as e:
        print(f" Error setting up Supabase: {e}")
        return False

def run_data_feeding():
    """Run the data feeding process"""
    print("\n Running data feeding...")
    
    try:
        # Run the data feeder
        os.system("python feed_data.py")
        return True
    except Exception as e:
        print(f" Error feeding data: {e}")
        return False

def main():
    """Main setup function"""
    print("Sign3T Automated Supabase Setup")
    print("=" * 50)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("\n Requirements not met. Please fix the issues above.")
        return False
    
    # Step 2: Setup Supabase tables
    if not setup_supabase_tables():
        print("\n Supabase setup failed.")
        return False
    
    # Step 3: Feed data
    print("\n Ready to feed data to Supabase!")
    print("Run the following command to feed your JSON data:")
    print("python feed_data.py")
    
    # Ask if user wants to run it now
    response = input("\nDo you want to run data feeding now? (y/n): ").lower().strip()
    if response == 'y':
        if run_data_feeding():
            print("\n Setup completed successfully!")
            print(" Your Sign3T website is ready!")
            print(" Run: ./run.sh")
        else:
            print("\n Data feeding failed.")
    else:
        print("\n Manual steps:")
        print("1. Run: python feed_data.py")
        print("2. Run: ./run.sh")
        print("3. Open: http://localhost:8501")
    
    return True

if __name__ == "__main__":
    main()
