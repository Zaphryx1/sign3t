#!/usr/bin/env python3
"""
Automated Supabase Table Creation and Data Feeding for Sign3T
This script automatically creates tables from JSON data files and feeds them to Supabase
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supabase_config import supabase_manager
from sentence_transformers import SentenceTransformer

class AutomatedSupabaseManager:
    """Automatically creates tables and feeds data from JSON files to Supabase"""
    
    def __init__(self):
        self.supabase = supabase_manager
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data_dir = "data"
        
    def create_automated_tables(self):
        """Create tables automatically based on JSON data structure"""
        if not self.supabase.is_connected():
            print("ERROR: Supabase not connected. Cannot create tables.")
            return False
            
        try:
            # Read the SQL schema file and execute it
            with open('supabase_schema.sql', 'r') as f:
                schema_sql = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.upper().startswith(('CREATE', 'INSERT', 'DROP')):
                    try:
                        # Execute the statement
                        result = self.supabase.client.rpc('exec_sql', {'sql': statement}).execute()
                        print(f" Executed: {statement[:50]}...")
                    except Exception as e:
                        print(f" Warning executing statement: {e}")
            
            print(" Automated table creation completed")
            return True
            
        except Exception as e:
            print(f" Error creating tables: {e}")
            return False
    
    def load_and_process_json_data(self):
        """Load all JSON data files and process them for Supabase"""
        json_files = {
            'dispatch_records': 'dispatch_records.json',
            'gis_data': 'gis_data.json', 
            'prior_incidents': 'prior_incidents.json',
            'sample_transcripts': 'sample_transcripts.json'
        }
        
        processed_data = {}
        
        for data_type, filename in json_files.items():
            filepath = os.path.join(self.data_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    processed_data[data_type] = data
                    print(f" Loaded {len(data)} records from {filename}")
                except Exception as e:
                    print(f" Error loading {filename}: {e}")
            else:
                print(f" File not found: {filepath}")
                
        return processed_data
    
    def feed_dispatch_records_to_supabase(self, dispatch_data: List[Dict]):
        """Feed dispatch records data to Supabase"""
        if not self.supabase.is_connected():
            print("WARNING: Supabase not connected. Skipping dispatch records.")
            return
            
        print(f" Feeding {len(dispatch_data)} dispatch records to Supabase...")
        
        for record in dispatch_data:
            try:
                # Create document entry for vector search
                content = f"Dispatch: {record.get('description', '')} - {record.get('call_type', '')}"
                metadata = {
                    "call_id": record.get('call_id', ''),
                    "location": record.get('location', ''),
                    "timestamp": record.get('timestamp', ''),
                    "call_type": record.get('call_type', ''),
                    "priority": record.get('priority', ''),
                    "response_time": record.get('response_time', ''),
                    "outcome": record.get('outcome', '')
                }
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Store in documents table
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="dispatch_records"
                )
                
                # Store in incidents table
                incident_data = {
                    "incident_id": record.get('call_id', ''),
                    "location": record.get('location', ''),
                    "incident_type": record.get('call_type', ''),
                    "severity": record.get('priority', 'MEDIUM').upper(),
                    "description": record.get('description', ''),
                    "suspects": json.dumps(record.get('suspects', [])),
                    "victims": json.dumps(record.get('victims', [])),
                    "weapons_involved": json.dumps(record.get('weapons_involved', [])),
                    "outcome": record.get('outcome', ''),
                    "officer_notes": record.get('officer_notes', ''),
                    "incident_data": json.dumps(record)
                }
                
                self.supabase.client.table("incidents").insert(incident_data).execute()
                
            except Exception as e:
                print(f" Error processing dispatch record {record.get('call_id', 'unknown')}: {e}")
        
        print(" Dispatch records fed to Supabase")
    
    def feed_gis_data_to_supabase(self, gis_data: List[Dict]):
        """Feed GIS data to Supabase"""
        if not self.supabase.is_connected():
            print("WARNING: Supabase not connected. Skipping GIS data.")
            return
            
        print(f" Feeding {len(gis_data)} GIS records to Supabase...")
        
        for record in gis_data:
            try:
                # Create document entry for vector search
                content = f"Location: {record.get('location', '')} - Type: {record.get('location_type', '')} - Crime History: {', '.join(record.get('crime_history', []))}"
                metadata = {
                    "location": record.get('location', ''),
                    "location_type": record.get('location_type', ''),
                    "crime_history": record.get('crime_history', []),
                    "risk_factors": record.get('risk_factors', []),
                    "access_points": record.get('access_points', 0),
                    "escape_routes": record.get('escape_routes', 0),
                    "nearby_landmarks": record.get('nearby_landmarks', []),
                    "population_density": record.get('population_density', ''),
                    "socioeconomic_status": record.get('socioeconomic_status', '')
                }
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Store in documents table
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="gis_maps"
                )
                
            except Exception as e:
                print(f" Error processing GIS record {record.get('location', 'unknown')}: {e}")
        
        print(" GIS data fed to Supabase")
    
    def feed_prior_incidents_to_supabase(self, incidents_data: List[Dict]):
        """Feed prior incidents data to Supabase"""
        if not self.supabase.is_connected():
            print("WARNING: Supabase not connected. Skipping prior incidents.")
            return
            
        print(f" Feeding {len(incidents_data)} prior incidents to Supabase...")
        
        for record in incidents_data:
            try:
                # Create document entry for vector search
                content = f"Incident: {record.get('description', '')} - Type: {record.get('incident_type', '')} - Severity: {record.get('severity', '')}"
                metadata = {
                    "incident_id": record.get('incident_id', ''),
                    "location": record.get('location', ''),
                    "date": record.get('date', ''),
                    "incident_type": record.get('incident_type', ''),
                    "severity": record.get('severity', ''),
                    "suspects": record.get('suspects', []),
                    "victims": record.get('victims', []),
                    "weapons_involved": record.get('weapons_involved', []),
                    "outcome": record.get('outcome', ''),
                    "officer_notes": record.get('officer_notes', '')
                }
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Store in documents table
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="prior_incidents"
                )
                
                # Store in incidents table
                incident_data = {
                    "incident_id": record.get('incident_id', ''),
                    "location": record.get('location', ''),
                    "incident_type": record.get('incident_type', ''),
                    "severity": record.get('severity', 'MEDIUM').upper(),
                    "description": record.get('description', ''),
                    "suspects": json.dumps(record.get('suspects', [])),
                    "victims": json.dumps(record.get('victims', [])),
                    "weapons_involved": json.dumps(record.get('weapons_involved', [])),
                    "outcome": record.get('outcome', ''),
                    "officer_notes": record.get('officer_notes', ''),
                    "incident_data": json.dumps(record)
                }
                
                self.supabase.client.table("incidents").insert(incident_data).execute()
                
            except Exception as e:
                print(f" Error processing incident {record.get('incident_id', 'unknown')}: {e}")
        
        print(" Prior incidents fed to Supabase")
    
    def feed_sample_transcripts_to_supabase(self, transcripts_data: List[Dict]):
        """Feed sample transcripts data to Supabase"""
        if not self.supabase.is_connected():
            print("WARNING: Supabase not connected. Skipping transcripts.")
            return
            
        print(f" Feeding {len(transcripts_data)} transcripts to Supabase...")
        
        for record in transcripts_data:
            try:
                # Create document entry for vector search
                content = record.get('text', '')
                metadata = record.get('metadata', {})
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Store in documents table
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="911_calls"
                )
                
            except Exception as e:
                print(f" Error processing transcript: {e}")
        
        print(" Sample transcripts fed to Supabase")
    
    def run_full_automation(self):
        """Run the complete automation process"""
        print(" Starting Automated Supabase Table Creation and Data Feeding")
        print("=" * 70)
        
        # Step 1: Create tables
        print("\n1 Creating automated tables...")
        if not self.create_automated_tables():
            print(" Failed to create tables. Exiting.")
            return False
        
        # Step 2: Load JSON data
        print("\n2 Loading JSON data files...")
        processed_data = self.load_and_process_json_data()
        
        if not processed_data:
            print(" No data loaded. Exiting.")
            return False
        
        # Step 3: Feed data to Supabase
        print("\n3 Feeding data to Supabase...")
        
        if 'dispatch_records' in processed_data:
            self.feed_dispatch_records_to_supabase(processed_data['dispatch_records'])
        
        if 'gis_data' in processed_data:
            self.feed_gis_data_to_supabase(processed_data['gis_data'])
        
        if 'prior_incidents' in processed_data:
            self.feed_prior_incidents_to_supabase(processed_data['prior_incidents'])
        
        if 'sample_transcripts' in processed_data:
            self.feed_sample_transcripts_to_supabase(processed_data['sample_transcripts'])
        
        # Step 4: Verify data
        print("\n4 Verifying data in Supabase...")
        self.verify_data_in_supabase()
        
        print("\n Automated Supabase setup completed successfully!")
        print(" Your Sign3T website can now access all the data!")
        return True
    
    def verify_data_in_supabase(self):
        """Verify that data was successfully stored in Supabase"""
        if not self.supabase.is_connected():
            print("WARNING: Cannot verify data - Supabase not connected.")
            return
        
        try:
            # Check documents table
            docs_result = self.supabase.client.table("documents").select("count").execute()
            print(f" Documents table: {len(docs_result.data)} records")
            
            # Check incidents table
            incidents_result = self.supabase.client.table("incidents").select("count").execute()
            print(f" Incidents table: {len(incidents_result.data)} records")
            
            # Check threat assessments table
            assessments_result = self.supabase.client.table("threat_assessments").select("count").execute()
            print(f" Threat assessments table: {len(assessments_result.data)} records")
            
            # Show data by source
            sources_result = self.supabase.client.table("documents").select("source").execute()
            if sources_result.data:
                source_counts = {}
                for record in sources_result.data:
                    source = record.get('source', 'unknown')
                    source_counts[source] = source_counts.get(source, 0) + 1
                
                print("\n Data by source:")
                for source, count in source_counts.items():
                    print(f"    {source}: {count} records")
            
        except Exception as e:
            print(f" Error verifying data: {e}")

def main():
    """Main function to run the automation"""
    print("Sign3T Automated Supabase Setup")
    print("=" * 50)
    
    # Initialize the automation manager
    automation_manager = AutomatedSupabaseManager()
    
    # Check if Supabase is connected
    if not automation_manager.supabase.is_connected():
        print(" Supabase not connected!")
        print("Please check your .env file and ensure Supabase credentials are correct.")
        print("Refer to SUPABASE_SETUP.md for setup instructions.")
        return False
    
    # Run the full automation
    success = automation_manager.run_full_automation()
    
    if success:
        print("\n Success! Your Sign3T system is now fully automated!")
        print(" You can now run: ./run.sh")
        print(" Open your browser to: http://localhost:8501")
    else:
        print("\n Automation failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
