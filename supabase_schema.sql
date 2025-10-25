-- Sign3T Database Schema for Supabase
-- This file contains the SQL schema needed for the Sign3T threat assessment system

-- Fix Sign3T Database Schema
-- Run this in Supabase SQL Editor to fix the database

-- First, drop existing tables if they exist (to start fresh)
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS threat_assessments CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;

-- Enable the pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table for storing text content with embeddings
CREATE TABLE documents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(384), -- 384 dimensions for sentence-transformers
    source VARCHAR(50) NOT NULL, -- '911_calls', 'prior_incidents', 'gis_maps', 'dispatch'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX documents_embedding_idx ON documents 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Create index for source filtering
CREATE INDEX documents_source_idx ON documents (source);

-- Create index for metadata queries
CREATE INDEX documents_metadata_idx ON documents USING GIN (metadata);

-- Threat assessments table
CREATE TABLE threat_assessments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    location VARCHAR(255) NOT NULL,
    threat_level VARCHAR(20) NOT NULL CHECK (threat_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    threat_score INTEGER NOT NULL CHECK (threat_score >= 0 AND threat_score <= 10),
    confidence_score DECIMAL(3,2) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    risk_factors JSONB DEFAULT '[]',
    weapons_involved JSONB DEFAULT '[]',
    known_individuals JSONB DEFAULT '[]',
    de_escalation_recommendations JSONB DEFAULT '[]',
    safety_protocols JSONB DEFAULT '[]',
    location_risks JSONB DEFAULT '[]',
    historical_context TEXT,
    assessment_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for threat assessments
CREATE INDEX threat_assessments_location_idx ON threat_assessments (location);
CREATE INDEX threat_assessments_threat_level_idx ON threat_assessments (threat_level);
CREATE INDEX threat_assessments_created_at_idx ON threat_assessments (created_at DESC);

-- Incidents table for storing incident reports
CREATE TABLE incidents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    incident_id VARCHAR(100) UNIQUE NOT NULL,
    location VARCHAR(255) NOT NULL,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    description TEXT NOT NULL,
    suspects JSONB DEFAULT '[]',
    victims JSONB DEFAULT '[]',
    weapons_involved JSONB DEFAULT '[]',
    outcome TEXT,
    officer_notes TEXT,
    incident_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for incidents
CREATE INDEX incidents_location_idx ON incidents (location);
CREATE INDEX incidents_type_idx ON incidents (incident_type);
CREATE INDEX incidents_severity_idx ON incidents (severity);
CREATE INDEX incidents_created_at_idx ON incidents (created_at DESC);

-- Function to search documents using vector similarity
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding VECTOR(384),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    metadata JSONB,
    source VARCHAR(50),
    similarity FLOAT,
    created_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE SQL
AS $$
    SELECT 
        d.id,
        d.content,
        d.metadata,
        d.source,
        1 - (d.embedding <=> query_embedding) AS similarity,
        d.created_at
    FROM documents d
    WHERE 1 - (d.embedding <=> query_embedding) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
$$;

-- Function to get recent threat assessments for a location
CREATE OR REPLACE FUNCTION get_recent_assessments(
    target_location VARCHAR(255),
    limit_count INT DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    location VARCHAR(255),
    threat_level VARCHAR(20),
    threat_score INTEGER,
    confidence_score DECIMAL(3,2),
    risk_factors JSONB,
    created_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE SQL
AS $$
    SELECT 
        ta.id,
        ta.location,
        ta.threat_level,
        ta.threat_score,
        ta.confidence_score,
        ta.risk_factors,
        ta.created_at
    FROM threat_assessments ta
    WHERE ta.location ILIKE '%' || target_location || '%'
    ORDER BY ta.created_at DESC
    LIMIT limit_count;
$$;

-- Function to get incident history for a location
CREATE OR REPLACE FUNCTION get_incident_history(
    target_location VARCHAR(255),
    days_back INT DEFAULT 30
)
RETURNS TABLE (
    id UUID,
    incident_id VARCHAR(100),
    location VARCHAR(255),
    incident_type VARCHAR(100),
    severity VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE SQL
AS $$
    SELECT 
        i.id,
        i.incident_id,
        i.location,
        i.incident_type,
        i.severity,
        i.description,
        i.created_at
    FROM incidents i
    WHERE i.location ILIKE '%' || target_location || '%'
    AND i.created_at >= NOW() - INTERVAL '1 day' * days_back
    ORDER BY i.created_at DESC;
$$;

-- Insert sample data for testing
INSERT INTO documents (content, metadata, source) VALUES
('Caller reports shouting and glass breaking. Suspect has prior assault charges.', 
 '{"location": "123 Main St", "call_id": "CALL001", "priority": "high"}', 
 '911_calls'),
('Drug activity reported. Known dealer operating from apartment complex. Undercover operation in progress. Known drug dealer location.', 
 '{"location": "777 Maple Dr", "incident_id": "INC-2024-002", "severity": "medium"}', 
 'prior_incidents'),
('Sexual assault reported. Victim seeking immediate help and protection.', 
 '{"address": "444 Campus Ave", "location_type": "educational", "crime_history": ["stalking"]}', 
 'gis_maps');

-- Insert sample threat assessment
INSERT INTO threat_assessments (location, threat_level, threat_score, confidence_score, risk_factors, weapons_involved, known_individuals) VALUES
('123 Main St', 'HIGH', 3, 0.85, 
 '["History of violence", "Weapons involved", "Mental health crisis"]'::jsonb,
 '["knife", "firearm"]'::jsonb,
 '[{"name": "John Doe", "role": "suspect", "risk_level": "high"}]'::jsonb),
 ('777 Maple Dr', 'MEDIUM', 2, 0.50, 
 '["drug_activity", "theft", "domestic_violence"]'::jsonb,
 '["knife"]'::jsonb,
 '[{"name": "Mason Lane", "role": "suspect", "risk_level": "medium"}]'::jsonb),
 ('444 Campus Ave', 'CRITICAL', 4, 0.99, 
 '["Restraining order issued, suspect arrested for violation", "Weapons involved", "Mental health crisis"]'::jsonb,
 '["tireiron"]'::jsonb,
 '[{"name": "David Brown", "role": "suspect", "risk_level": "critical"}]'::jsonb);

-- Insert sample incident
INSERT INTO incidents (incident_id, location, incident_type, severity, description, suspects, weapons_involved) VALUES
('INC-2024-001', '123 Main St', 'domestic_violence', 'HIGH', 
 'Domestic violence incident involving physical assault. Suspect arrested for battery.',
 '["John Doe"]'::jsonb,
 '["knife"]'::jsonb),
 ('INC-2024-004', '777 Maple Dr', 'drug_activity', 'MEDIUM', 
 'Drug dealing operation discovered in apartment complex.',
 '["Mason Lane"]'::jsonb,
 '["unarmed"]'::jsonb),
 ('INC-2024-009', '444 Campus Ave', 'stalking', 'MEDIUM', 
 'Stalking complaint. Ex-partner following victim and making threats.',
 '["David Brown"]'::jsonb,
 '["unarmed"]'::jsonb);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_threat_assessments_updated_at BEFORE UPDATE ON threat_assessments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_incidents_updated_at BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant necessary permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;