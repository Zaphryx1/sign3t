# Simplified version without LangChain for demo purposes
from threat_assessment import generate_threat_assessment, ThreatAssessment
from config import THREAT_LEVELS
import json

def format_threat_assessment(assessment: ThreatAssessment) -> str:
    """Format threat assessment into a comprehensive briefing"""
    
    # Get threat level info
    threat_info = THREAT_LEVELS.get(assessment.threat_level, {})
    threat_color = threat_info.get("color", "gray")
    threat_description = threat_info.get("description", "Unknown risk level")
    
    briefing = f"""
OFFICER THREAT BRIEFING
{'='*50}

LOCATION: {assessment.known_individuals[0].get('name', 'Unknown') if assessment.known_individuals else 'Unknown'}
ASSESSMENT TIME: {assessment.last_updated}
THREAT LEVEL: {assessment.threat_level} ({threat_description})
THREAT SCORE: {assessment.threat_score}/10
CONFIDENCE: {assessment.confidence_score:.1%}

RISK FACTORS:
"""
    
    for factor in assessment.risk_factors:
        briefing += f"• {factor}\n"
    
    if assessment.weapons_involved:
        briefing += f"\nWEAPONS INVOLVED:\n"
        for weapon in assessment.weapons_involved:
            briefing += f"• {weapon}\n"
    
    if assessment.known_individuals:
        briefing += f"\nKNOWN INDIVIDUALS:\n"
        for person in assessment.known_individuals:
            briefing += f"• {person['name']} ({person['role']}) - Risk: {person['risk_level']}\n"
            briefing += f"  History: {person['history']}\n"
    
    if assessment.location_risks:
        briefing += f"\nLOCATION RISKS:\n"
        for risk in assessment.location_risks:
            briefing += f"• {risk}\n"
    
    briefing += f"\nDE-ESCALATION RECOMMENDATIONS:\n"
    for i, rec in enumerate(assessment.de_escalation_recommendations, 1):
        briefing += f"{i}. {rec}\n"
    
    briefing += f"\nSAFETY PROTOCOLS:\n"
    for i, protocol in enumerate(assessment.safety_protocols, 1):
        briefing += f"{i}. {protocol}\n"
    
    if assessment.historical_context:
        briefing += f"\nHISTORICAL CONTEXT:\n{assessment.historical_context}\n"
    
    briefing += f"\n{'='*50}"
    briefing += f"\nRemember: This assessment is AI-generated and should be used as a guide. Always use your training and judgment in the field."
    
    return briefing

def generate_briefing(location):
    """Generate comprehensive threat briefing for officers"""
    try:
        # Generate threat assessment
        assessment = generate_threat_assessment(location)
        
        # Format into briefing
        briefing = format_threat_assessment(assessment)
        
        return briefing
        
    except Exception as e:
        return f"Error generating briefing: {str(e)}\n\nPlease check your data sources and try again."