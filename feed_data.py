#!/usr/bin/env python3
"""
Simple Automated Supabase Data Feeder for Sign3T
This script automatically feeds JSON data to Supabase tables
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from supabase_config import supabase_manager
from sentence_transformers import SentenceTransformer

class SimpleDataFeeder:
    """Simple data feeder for Supabase"""
    
    def __init__(self):
        self.supabase = supabase_manager
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data_dir = "data"
        
    def load_json_file(self, filename: str) -> List[Dict]:
        """Load a JSON file and return the data"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File not found: {filepath}")
            return []
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} records from {filename}")
            return data
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def feed_dispatch_records(self):
        """Feed dispatch records to Supabase"""
        data = self.load_json_file('dispatch_records.json')
        
        if not data or not self.supabase.is_connected():
            return
        
        print(f"Feeding {len(data)} dispatch records...")
        
        for record in data:
            try:
                # Create document for vector search
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
                
                # Store document
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="dispatch_records"
                )
                
                # Store as incident (with duplicate handling)
                incident_data = {
                    "incident_id": record.get('call_id', ''),
                    "location": record.get('location', ''),
                    "incident_type": record.get('call_type', ''),
                    "severity": record.get('priority', 'MEDIUM').upper(),
                    "description": record.get('description', ''),
                    "outcome": record.get('outcome', ''),
                    "officer_notes": record.get('officer_notes', ''),
                    "incident_data": json.dumps(record)
                }
                
                # Use upsert to handle duplicates
                self.supabase.client.table("incidents").upsert(incident_data).execute()
                
            except Exception as e:
                print(f"Warning: Error processing dispatch record: {e}")
        
        print("Dispatch records fed successfully")
    
    def feed_gis_data(self):
        """Feed GIS data to Supabase"""
        data = self.load_json_file('gis_data.json')
        
        if not data or not self.supabase.is_connected():
            return
        
        print(f"Feeding {len(data)} GIS records...")
        
        for record in data:
            try:
                # Create document for vector search
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
                
                # Store document
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="gis_maps"
                )
                
            except Exception as e:
                print(f"Warning: Error processing GIS record: {e}")
        
        print("GIS data fed successfully")
    
    def feed_prior_incidents(self):
        """Feed prior incidents to Supabase"""
        data = self.load_json_file('prior_incidents.json')
        
        if not data or not self.supabase.is_connected():
            return
        
        print(f"Feeding {len(data)} prior incidents...")
        
        for record in data:
            try:
                # Create document for vector search
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
                
                # Store document
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="prior_incidents"
                )
                
                # Store as incident (with duplicate handling)
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
                
                # Use upsert to handle duplicates
                self.supabase.client.table("incidents").upsert(incident_data).execute()
                
            except Exception as e:
                print(f"Warning: Error processing incident: {e}")
        
        print("Prior incidents fed successfully")
    
    def feed_sample_transcripts(self):
        """Feed sample transcripts to Supabase"""
        data = self.load_json_file('sample_transcripts.json')
        
        if not data or not self.supabase.is_connected():
            return
        
        print(f"Feeding {len(data)} transcripts...")
        
        for record in data:
            try:
                # Create document for vector search
                content = record.get('text', '')
                metadata = record.get('metadata', {})
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                # Store document
                self.supabase.store_document(
                    content=content,
                    metadata=metadata,
                    embedding=embedding,
                    source="911_calls"
                )
                
            except Exception as e:
                print(f"Warning: Error processing transcript: {e}")
        
        print("Sample transcripts fed successfully")
    
    def run_data_feeding(self):
        """Run the complete data feeding process"""
        print("Starting Automated Data Feeding to Supabase")
        print("=" * 60)
        
        if not self.supabase.is_connected():
            print("Supabase not connected!")
            print("Please check your .env file and Supabase credentials.")
            return False
        
        print("Supabase connected successfully")
        
        # Feed all data types
        self.feed_dispatch_records()
        self.feed_gis_data()
        self.feed_prior_incidents()
        self.feed_sample_transcripts()
        
        # Verify data
        print("\nVerifying data in Supabase...")
        self.verify_data()
        
        print("\nData feeding completed successfully!")
        print("Your Sign3T website now has access to all data!")
        return True
    
    def verify_data(self):
        """Verify data was stored successfully"""
        try:
            # Check documents count
            docs_result = self.supabase.client.table("documents").select("source").execute()
            if docs_result.data:
                source_counts = {}
                for record in docs_result.data:
                    source = record.get('source', 'unknown')
                    source_counts[source] = source_counts.get(source, 0) + 1
                
                print("Documents by source:")
                for source, count in source_counts.items():
                    print(f"    {source}: {count} records")
            
            # Check incidents count
            incidents_result = self.supabase.client.table("incidents").select("count").execute()
            print(f"Total incidents: {len(incidents_result.data)} records")
            
        except Exception as e:
            print(f"Warning: Error verifying data: {e}")

def main():
    """Main function"""
    print("Sign3T Simple Data Feeder")
    print("=" * 40)
    
    feeder = SimpleDataFeeder()
    success = feeder.run_data_feeding()
    
    if success:
        print("\nSuccess! Data feeding completed!")
        print("Run your website: ./run.sh")
        print("Open browser to: http://localhost:8501")
    else:
        print("\nData feeding failed. Check errors above.")

if __name__ == "__main__":
    main()
