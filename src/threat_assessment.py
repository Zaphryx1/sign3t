import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from config import THREAT_LEVELS
from local_ai import local_ai
from supabase_config import supabase_manager
from sentence_transformers import SentenceTransformer

@dataclass
class ThreatAssessment:
    """Data class for threat assessment results"""
    threat_level: str
    threat_score: int
    risk_factors: List[str]
    known_individuals: List[Dict]
    weapons_involved: List[str]
    de_escalation_recommendations: List[str]
    safety_protocols: List[str]
    location_risks: List[str]
    historical_context: str
    confidence_score: float
    last_updated: str

class AdvancedThreatAssessment:
    """Advanced AI-driven threat assessment system"""
    
    def __init__(self):
        # Use local AI instead of cloud APIs
        self.local_ai = local_ai
        
        # Threat indicators and their weights
        self.threat_indicators = {
            "weapons_mentioned": 0.8,
            "violence_history": 0.7,
            "domestic_violence": 0.6,
            "mental_health_crisis": 0.5,
            "substance_abuse": 0.4,
            "barricaded_subject": 0.9,
            "hostage_situation": 1.0,
            "active_shooter": 1.0,
            "explosive_threat": 0.95,
            "gang_activity": 0.6,
            "terrorism_indicators": 0.9
        }
        
        # De-escalation strategies
        self.de_escalation_strategies = {
            "domestic_violence": [
                "Separate parties immediately",
                "Use calm, non-threatening language",
                "Avoid taking sides",
                "Ensure victim safety first",
                "Document all injuries and statements"
            ],
            "mental_health_crisis": [
                "Speak slowly and clearly",
                "Maintain safe distance",
                "Avoid sudden movements",
                "Use de-escalation techniques",
                "Consider crisis intervention team"
            ],
            "weapons_involved": [
                "Establish perimeter",
                "Request backup immediately",
                "Use cover and concealment",
                "Avoid direct confrontation",
                "Consider SWAT if necessary"
            ],
            "barricaded_subject": [
                "Secure perimeter",
                "Evacuate nearby residents",
                "Establish command post",
                "Use negotiation techniques",
                "Prepare for tactical entry"
            ]
        }
    
    def get_relevant_documents(self, location: str) -> List[Dict]:
        """Retrieve relevant documents from Supabase for the location"""
        if not supabase_manager.is_connected():
            # Fallback to diverse mock data based on location
            return self._get_diverse_mock_data(location)
        
        try:
            # Generate embedding for the location query
            embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = embedding_model.encode(f"threat assessment {location}").tolist()
            
            # Search for relevant documents
            documents = supabase_manager.search_documents(query_embedding, limit=10)
            
            # Filter by location if possible
            location_docs = []
            for doc in documents:
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                if (isinstance(content, str) and location.lower() in content.lower()) or \
                   (isinstance(metadata, dict) and location.lower() in str(metadata).lower()):
                    location_docs.append(doc)
            
            return location_docs if location_docs else documents[:3]
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def _get_diverse_mock_data(self, location: str) -> List[Dict]:
        """Generate diverse mock data based on location patterns"""
        import random
        
        # Load diverse data files
        try:
            with open('data/sample_transcripts.json', 'r') as f:
                transcripts = json.load(f)
        except:
            transcripts = []
            
        try:
            with open('data/prior_incidents.json', 'r') as f:
                incidents = json.load(f)
        except:
            incidents = []
            
        try:
            with open('data/gis_data.json', 'r') as f:
                gis_data = json.load(f)
        except:
            gis_data = []
            
        try:
            with open('data/dispatch_records.json', 'r') as f:
                dispatch = json.load(f)
        except:
            dispatch = []
        
        # Find location-specific data
        location_docs = []
        
        # Add 911 calls for this location
        for transcript in transcripts:
            if location.lower() in transcript.get('metadata', {}).get('location', '').lower():
                location_docs.append({
                    "content": transcript['text'],
                    "metadata": transcript['metadata']
                })
        
        # Add prior incidents for this location
        for incident in incidents:
            if location.lower() in incident.get('location', '').lower():
                location_docs.append({
                    "content": f"Previous incident: {incident['description']}",
                    "metadata": {
                        "source": "prior_incidents",
                        "location": incident['location'],
                        "incident_type": incident['incident_type'],
                        "severity": incident['severity']
                    }
                })
        
        # Add GIS data for this location
        for gis in gis_data:
            if location.lower() in gis.get('location', '').lower():
                risk_factors = ", ".join(gis.get('risk_factors', []))
                crime_history = ", ".join(gis.get('crime_history', []))
                location_docs.append({
                    "content": f"Location analysis: {gis['location_type']} with risk factors: {risk_factors}. Crime history: {crime_history}",
                    "metadata": {
                        "source": "gis_maps",
                        "location": gis['location'],
                        "location_type": gis['location_type']
                    }
                })
        
        # Add dispatch records for this location
        for record in dispatch:
            if location.lower() in record.get('location', '').lower():
                location_docs.append({
                    "content": f"Dispatch: {record['description']}",
                    "metadata": {
                        "source": "dispatch",
                        "location": record['location'],
                        "call_type": record['call_type'],
                        "priority": record['priority']
                    }
                })
        
        # If no specific data found, return diverse random samples
        if not location_docs:
            all_docs = []
            all_docs.extend(transcripts[:3])
            all_docs.extend(incidents[:2])
            all_docs.extend(gis_data[:2])
            all_docs.extend(dispatch[:2])
            
            # Randomly select diverse samples
            random.shuffle(all_docs)
            for doc in all_docs[:5]:
                if 'text' in doc:
                    location_docs.append({
                        "content": doc['text'],
                        "metadata": doc.get('metadata', {})
                    })
                elif 'description' in doc:
                    location_docs.append({
                        "content": doc['description'],
                        "metadata": {
                            "source": "prior_incidents",
                            "location": doc.get('location', location),
                            "incident_type": doc.get('incident_type', 'unknown')
                        }
                    })
                elif 'location_type' in doc:
                    location_docs.append({
                        "content": f"Location: {doc['location']} - {doc['location_type']} with risks: {', '.join(doc.get('risk_factors', []))}",
                        "metadata": {
                            "source": "gis_maps",
                            "location": doc['location']
                        }
                    })
        
        return location_docs[:8]  # Return up to 8 diverse documents

    def analyze_threat_indicators(self, location: str) -> Dict[str, Any]:
        """Analyze threat indicators from all data sources using local AI"""
        # Get relevant documents from Supabase
        documents = self.get_relevant_documents(location)
        
        # Combine document content for context
        context_parts = [doc['content'] for doc in documents]
        context = f"Location: {location}. " + " ".join(context_parts)
        
        response = self.local_ai.analyze_threat(location, context)
        
        # Handle both dict and string responses
        if isinstance(response, dict):
            # Extract from structured response
            threat_factors = response.get("threat_factors", [])
            weapons = response.get("weapons", [])
            violence_history = response.get("violence_history", [])
            mental_health_indicators = response.get("mental_health_indicators", False)
            raw_response = str(response)
        else:
            # Handle string response with regex parsing
            raw_response = str(response)
            threat_factors = []
            weapons = []
            violence_history = []
            mental_health_indicators = False

            if "weapons mentioned" in raw_response.lower() or "weapon involved" in raw_response.lower():
                threat_factors.append("Weapons involved")
                weapons.append("Unknown weapon") # Placeholder
            if "violence history present" in raw_response.lower() or "assault charges" in raw_response.lower() or "domestic violence" in raw_response.lower():
                threat_factors.append("History of violence")
                violence_history.append("Prior assault charges") # Placeholder
            if "mental health concerns" in raw_response.lower() or "mental health crisis" in raw_response.lower():
                threat_factors.append("Mental health crisis")
                mental_health_indicators = True

        return {
            "threat_factors": threat_factors,
            "weapons": weapons,
            "violence_history": violence_history,
            "mental_health_indicators": mental_health_indicators,
            "raw_response": response,
            "source_documents": documents
        }
    
    def calculate_threat_score(self, indicators: Dict[str, Any]) -> Tuple[int, str]:
        """Calculate threat score based on indicators"""
        score = 0
        risk_factors = []
        
        # Weapons involved - check multiple possible keys
        weapons = indicators.get("weapons", []) or indicators.get("weapons_involved", [])
        if weapons:
            score += 3
            risk_factors.append("Weapons involved")
        
        # Violence history - check multiple possible keys
        violence_history = indicators.get("violence_history", []) or indicators.get("risk_factors", [])
        if violence_history and any("violence" in str(item).lower() for item in violence_history):
            score += 2
            risk_factors.append("History of violence")
        
        # Mental health crisis - check multiple possible keys
        mental_health = indicators.get("mental_health_indicators", []) or indicators.get("mental_health_concerns", False)
        if mental_health or (violence_history and any("mental" in str(item).lower() for item in violence_history)):
            score += 2
            risk_factors.append("Mental health crisis")
        
        # Determine threat level
        if score >= 6:
            threat_level = "CRITICAL"
        elif score >= 4:
            threat_level = "HIGH"
        elif score >= 2:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        return score, threat_level
    
    def get_known_individuals(self, location: str) -> List[Dict]:
        """Extract known individuals from the data"""
        # For demo purposes, return sample data
        
        # This would typically parse structured data, but for demo we'll return sample data
        return [
            {
                "name": "John Doe",
                "role": "suspect",
                "history": "Previous assault charges",
                "risk_level": "high",
                "last_seen": "2024-01-15"
            },
            {
                "name": "Jane Doe", 
                "role": "victim",
                "history": "Previous victim of domestic violence",
                "risk_level": "medium",
                "last_seen": "2024-01-15"
            }
        ]
    
    def generate_de_escalation_recommendations(self, threat_level: str, incident_type: str) -> List[str]:
        """Generate de-escalation recommendations based on threat level and incident type"""
        recommendations = []
        
        # Base recommendations for all situations
        recommendations.extend([
            "Maintain situational awareness",
            "Communicate clearly with dispatch",
            "Document all observations",
            "Ensure officer safety first"
        ])
        
        # Specific recommendations based on incident type
        if incident_type in self.de_escalation_strategies:
            recommendations.extend(self.de_escalation_strategies[incident_type])
        
        # Additional recommendations based on threat level
        if threat_level == "CRITICAL":
            recommendations.extend([
                "Request immediate backup",
                "Consider SWAT deployment",
                "Establish secure perimeter",
                "Evacuate civilians if necessary"
            ])
        elif threat_level == "HIGH":
            recommendations.extend([
                "Request backup",
                "Use tactical approach",
                "Maintain cover and concealment"
            ])
        
        return recommendations
    
    def get_safety_protocols(self, threat_level: str) -> List[str]:
        """Get safety protocols based on threat level"""
        protocols = {
            "LOW": [
                "Standard patrol procedures",
                "Basic de-escalation techniques",
                "Document all interactions"
            ],
            "MEDIUM": [
                "Enhanced situational awareness",
                "Partner backup recommended",
                "Use of body camera mandatory"
            ],
            "HIGH": [
                "Multiple unit response",
                "Tactical approach required",
                "SWAT consideration",
                "Evacuation planning"
            ],
            "CRITICAL": [
                "Immediate SWAT deployment",
                "Full tactical response",
                "Emergency evacuation",
                "Command post establishment"
            ]
        }
        
        return protocols.get(threat_level, protocols["LOW"])
    
    def assess_location_risks(self, location: str) -> List[str]:
        """Assess location-specific risks"""
        # For demo purposes, return sample risks
        response = f"Location {location} has poor lighting, narrow access points, and limited evacuation routes."
        
        # Parse response for location risks
        risks = []
        if "poor lighting" in response.lower():
            risks.append("Poor lighting conditions")
        if "narrow" in response.lower():
            risks.append("Limited access points")
        if "residential" in response.lower():
            risks.append("Civilians in vicinity")
        
        return risks
    
    def get_historical_context(self, location: str) -> str:
        """Get historical context for the location"""
        # For demo purposes, return sample context
        return f"Previous incidents at {location} include domestic violence calls, assault reports, and noise complaints. Area has high crime rate."
    
    def calculate_confidence_score(self, indicators: Dict[str, Any]) -> float:
        """Calculate confidence score for the assessment"""
        # Simple confidence calculation based on data availability
        data_points = 0
        total_points = 5  # Maximum possible data points
        
        weapons = indicators.get("weapons", []) or indicators.get("weapons_involved", [])
        if weapons:
            data_points += 1
            
        violence_history = indicators.get("violence_history", []) or indicators.get("risk_factors", [])
        if violence_history:
            data_points += 1
            
        mental_health = indicators.get("mental_health_indicators", []) or indicators.get("mental_health_concerns", False)
        if mental_health:
            data_points += 1
            
        if indicators.get("raw_response"):
            data_points += 1
        if indicators.get("location_data"):
            data_points += 1
        
        return data_points / total_points
    
    def generate_comprehensive_assessment(self, location: str) -> ThreatAssessment:
        """Generate comprehensive threat assessment"""
        print(f"Generating threat assessment for {location}...")
        
        # Analyze threat indicators
        indicators = self.analyze_threat_indicators(location)
        
        # Calculate threat score and level
        threat_score, threat_level = self.calculate_threat_score(indicators)
        
        # Get additional information
        known_individuals = self.get_known_individuals(location)
        weapons_involved = indicators.get("weapons", []) or indicators.get("weapons_involved", [])
        location_risks = self.assess_location_risks(location)
        historical_context = self.get_historical_context(location)
        
        # Generate recommendations
        incident_type = "domestic_violence"  # This would be determined from the data
        de_escalation_recommendations = self.generate_de_escalation_recommendations(threat_level, incident_type)
        safety_protocols = self.get_safety_protocols(threat_level)
        
        # Calculate confidence
        confidence_score = self.calculate_confidence_score(indicators)
        
        # Create risk factors list
        risk_factors = []
        weapons = indicators.get("weapons", []) or indicators.get("weapons_involved", [])
        if weapons:
            risk_factors.append("Weapons involved")
            
        violence_history = indicators.get("violence_history", []) or indicators.get("risk_factors", [])
        if violence_history:
            risk_factors.append("History of violence")
            
        mental_health = indicators.get("mental_health_indicators", []) or indicators.get("mental_health_concerns", False)
        if mental_health:
            risk_factors.append("Mental health concerns")
        
        # Create threat assessment object
        assessment = ThreatAssessment(
            threat_level=threat_level,
            threat_score=threat_score,
            risk_factors=risk_factors,
            known_individuals=known_individuals,
            weapons_involved=weapons_involved,
            de_escalation_recommendations=de_escalation_recommendations,
            safety_protocols=safety_protocols,
            location_risks=location_risks,
            historical_context=historical_context,
            confidence_score=confidence_score,
            last_updated=datetime.now().isoformat()
        )
        
        # Store in Supabase if connected
        if supabase_manager.is_connected():
            try:
                assessment_data = {
                    "location": location,
                    "threat_level": threat_level,
                    "threat_score": threat_score,
                    "confidence_score": confidence_score,
                    "risk_factors": risk_factors,
                    "weapons_involved": weapons_involved,
                    "known_individuals": known_individuals,
                    "de_escalation_recommendations": de_escalation_recommendations,
                    "safety_protocols": safety_protocols,
                    "location_risks": location_risks,
                    "historical_context": historical_context,
                    "assessment_data": {
                        "raw_response": indicators.get("raw_response", ""),
                        "source_documents": indicators.get("source_documents", [])
                    }
                }
                supabase_manager.store_threat_assessment(assessment_data)
            except Exception as e:
                print(f"Warning: Could not store assessment in Supabase: {e}")
        
        return assessment

# Initialize threat assessment system
threat_assessor = AdvancedThreatAssessment()

def generate_threat_assessment(location: str) -> ThreatAssessment:
    """Generate comprehensive threat assessment for a location"""
    return threat_assessor.generate_comprehensive_assessment(location)
