"""
Supabase Configuration for Sign3T
Handles database connection and vector operations
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vuwyztuvovtfzktgkqei.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1d3l6dHV2b3Z0ZnprdGdrcWVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzNDcyMTAsImV4cCI6MjA3NjkyMzIxMH0.1NjxZg5dF0sX3VpluD8shC8YHXsRQrS3KLZy0QFc8A8")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1d3l6dHV2b3Z0ZnprdGdrcWVpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTM0NzIxMCwiZXhwIjoyMDc2OTIzMjEwfQ.l_tOw22WHy1mSnhVRVGj6m9NQ4bcoW4ZDmodBDaAkwM")

class SupabaseManager:
    """Manages Supabase database operations for Sign3T"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self._connect()
    
    def _connect(self):
        """Initialize Supabase client"""
        try:
            # Allow default credentials for testing
            if not SUPABASE_URL:
                print("WARNING  Supabase not configured. Using local mode.")
                return
                
            self.client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            print("Connected to Supabase")
        except Exception as e:
            print(f"Failed to connect to Supabase: {e}")
            print(" Using local mode - data will be stored in memory")
    
    def is_connected(self) -> bool:
        """Check if Supabase is connected"""
        return self.client is not None
    
    def create_tables(self):
        """Create necessary tables for Sign3T"""
        if not self.is_connected():
            print("WARNING  Supabase not connected. Skipping table creation.")
            return
        
        try:
            # Create documents table for vector storage
            self.client.rpc('create_documents_table').execute()
            
            # Create threat_assessments table
            self.client.rpc('create_threat_assessments_table').execute()
            
            # Create incidents table
            self.client.rpc('create_incidents_table').execute()
            
            print(" Database tables created successfully")
        except Exception as e:
            print(f" Error creating tables: {e}")
    
    def store_document(self, content: str, metadata: dict, embedding: list = None, source: str = "unknown"):
        """Store a document with optional embedding"""
        if not self.is_connected():
            print("WARNING  Supabase not connected. Document not stored.")
            return None
        
        try:
            document_data = {
                "content": content,
                "metadata": metadata,
                "embedding": embedding,
                "source": source
            }
            
            result = self.client.table("documents").insert(document_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f" Error storing document: {e}")
            return None
    
    def search_documents(self, query_embedding: list, limit: int = 5):
        """Search documents using vector similarity"""
        if not self.is_connected():
            print("WARNING  Supabase not connected. Returning empty results.")
            return []
        
        try:
            result = self.client.rpc(
                'search_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.1,  # Lower threshold to get more results
                    'match_count': limit
                }
            ).execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f" Error searching documents: {e}")
            return []
    
    def store_threat_assessment(self, assessment_data: dict):
        """Store threat assessment results"""
        if not self.is_connected():
            print("WARNING  Supabase not connected. Assessment not stored.")
            return None
        
        try:
            result = self.client.table("threat_assessments").insert(assessment_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f" Error storing threat assessment: {e}")
            return None
    
    def get_threat_assessments_by_location(self, location: str, limit: int = 10):
        """Get recent threat assessments for a location"""
        if not self.is_connected():
            print("WARNING  Supabase not connected. Returning empty results.")
            return []
        
        try:
            result = self.client.table("threat_assessments")\
                .select("*")\
                .eq("location", location)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            print(f" Error getting threat assessments: {e}")
            return []

# Global Supabase manager instance
supabase_manager = SupabaseManager()
