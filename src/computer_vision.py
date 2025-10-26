"""
Computer Vision Module for Sign3T
Handles image analysis, object detection, and threat classification from surveillance feeds.
"""

from PIL import Image
import cv2
import numpy as np
import random
from datetime import datetime
from typing import List, Dict, Any

class ComputerVisionAnalyzer:
    """
    Analyzes images from surveillance feeds for threat detection.
    Uses dummy logic for object detection and threat classification.
    """

    def __init__(self):
        self.threat_objects = {
            "weapon": {"level": "CRITICAL", "keywords": ["gun", "knife", "bomb", "firearm"]},
            "agitated behavior": {"level": "MEDIUM", "keywords": ["fighting", "shouting", "struggle"]},
            "multiple individuals": {"level": "MEDIUM", "keywords": ["crowd", "group", "gathering"]},
            "vehicle": {"level": "LOW", "keywords": ["car", "truck", "motorcycle"]},
            "person": {"level": "LOW", "keywords": ["individual", "human"]},
            "suspicious activity": {"level": "MEDIUM", "keywords": ["loitering", "unusual movement"]},
            "fire": {"level": "CRITICAL", "keywords": ["smoke", "flames"]},
            "medical emergency": {"level": "HIGH", "keywords": ["injury", "unconscious"]},
        }
        self.threat_level_mapping = {
            "CRITICAL": 10,
            "HIGH": 7,
            "MEDIUM": 4,
            "LOW": 1
        }

    def _simulate_object_detection(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Simulates object detection on an image.
        In a real scenario, this would use a pre-trained CV model.
        """
        # Dummy logic: return a random set of detected objects based on a "scene"
        # For demonstration, we'll use a fixed set of scenarios
        
        # Simulate different scenarios based on a dummy image path or random choice
        scenario_choice = random.choice([
            "active_shooter", "domestic_violence", "mental_health_crisis", "routine_patrol"
        ])

        if scenario_choice == "active_shooter":
            return [
                {"object": "weapon", "confidence": random.uniform(0.8, 0.95)},
                {"object": "multiple individuals", "confidence": random.uniform(0.7, 0.9)},
                {"object": "agitated behavior", "confidence": random.uniform(0.75, 0.98)},
            ]
        elif scenario_choice == "domestic_violence":
            return [
                {"object": "weapon", "confidence": random.uniform(0.6, 0.8)},
                {"object": "agitated behavior", "confidence": random.uniform(0.8, 0.95)},
                {"object": "person", "confidence": random.uniform(0.9, 0.99)},
            ]
        elif scenario_choice == "mental_health_crisis":
            return [
                {"object": "person", "confidence": random.uniform(0.9, 0.99)},
                {"object": "agitated behavior", "confidence": random.uniform(0.5, 0.7)},
            ]
        else: # routine_patrol
            return [
                {"object": "person", "confidence": random.uniform(0.8, 0.99)},
                {"object": "vehicle", "confidence": random.uniform(0.7, 0.9)},
            ]

    def analyze_surveillance_feed(self, image_path: str) -> Dict[str, Any]:
        """
        Analyzes a surveillance feed image for threats.
        Returns a structured dictionary of threat analysis.
        """
        detected_objects = self._simulate_object_detection(image_path)
        
        threat_detections = []
        overall_threat_score = 0
        max_threat_level = "LOW"
        
        for obj_data in detected_objects:
            obj_name = obj_data["object"]
            confidence = obj_data["confidence"]
            
            threat_info = self.threat_objects.get(obj_name)
            if threat_info:
                threat_level = threat_info["level"]
                threat_score = self.threat_level_mapping.get(threat_level, 0)
                
                threat_detections.append({
                    "object": obj_name,
                    "threat_level": threat_level,
                    "confidence": round(confidence * 100, 1),
                    "description": f"Detected {obj_name} with {threat_level} threat level"
                })
                
                overall_threat_score += threat_score * confidence
                
                # Update max threat level
                if self.threat_level_mapping.get(threat_level, 0) > self.threat_level_mapping.get(max_threat_level, 0):
                    max_threat_level = threat_level
        
        # Cap overall threat score at 10
        overall_threat_score = min(10, round(overall_threat_score / len(detected_objects) if detected_objects else 0))
        
        return {
            "timestamp": datetime.now().isoformat(),
            "image_path": image_path,
            "detected_objects": threat_detections,
            "overall_threat_level": max_threat_level,
            "threat_score": overall_threat_score,
            "total_detections": len(detected_objects),
            "threat_breakdown": self._get_threat_breakdown(threat_detections),
            "recommendations": self._generate_cv_recommendations(max_threat_level, threat_detections),
            "safety_protocols": self._generate_cv_safety_protocols(max_threat_level, threat_detections)
        }

    def _get_threat_breakdown(self, detections: List[Dict[str, Any]]) -> Dict[str, int]:
        """Counts detections by threat level."""
        breakdown = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for det in detections:
            breakdown[det["threat_level"]] += 1
        return breakdown

    def _generate_cv_recommendations(self, overall_threat_level: str, detections: List[Dict[str, Any]]) -> List[str]:
        """Generates recommendations based on CV analysis."""
        recommendations = []
        
        if overall_threat_level == "CRITICAL":
            recommendations.append("Immediate tactical response required")
            recommendations.append("Evacuate civilians from area")
            recommendations.append("Request specialized units (e.g., SWAT, Bomb Squad)")
        elif overall_threat_level == "HIGH":
            recommendations.append("Immediate backup requested - potential for violence")
            recommendations.append("Maintain safe distance and cover")
            recommendations.append("Prepare for de-escalation or use of force")
        elif overall_threat_level == "MEDIUM":
            recommendations.append("Monitor situation closely - potential for escalation")
            recommendations.append("Communicate with dispatch for additional context")
        
        for det in detections:
            if "weapon" in det["object"]:
                recommendations.append(f"Weapons detected: {det['object']} - proceed with extreme caution")
            if "agitated behavior" in det["object"]:
                recommendations.append("Approach with de-escalation techniques for agitated individuals")
            if "multiple individuals" in det["object"]:
                recommendations.append("Implement crowd control protocols if necessary")
        
        return list(set(recommendations)) # Remove duplicates

    def _generate_cv_safety_protocols(self, overall_threat_level: str, detections: List[Dict[str, Any]]) -> List[str]:
        """Generates safety protocols based on CV analysis."""
        protocols = []
        
        if overall_threat_level == "CRITICAL":
            protocols.append("Full tactical gear required")
            protocols.append("Backup units on standby")
            protocols.append("Evacuation procedures ready")
        elif overall_threat_level == "HIGH":
            protocols.append("Body armor and protective gear recommended")
            protocols.append("Maintain visual on all subjects")
        elif overall_threat_level == "MEDIUM":
            protocols.append("Standard patrol safety protocols")
        
        for det in detections:
            if "weapon" in det["object"]:
                protocols.append("Prioritize securing weapons")
            if "fire" in det["object"]:
                protocols.append("Alert fire department and prepare for fire suppression")
        
        return list(set(protocols)) # Remove duplicates

    def create_surveillance_report(self, image_path: str) -> str:
        """
        Generates a formatted surveillance report based on image analysis.
        """
        analysis = self.analyze_surveillance_feed(image_path)
        
        report = f"""
SURVEILLANCE ANALYSIS REPORT
==================================================

TIMESTAMP: {analysis['timestamp']}
IMAGE: {analysis['image_path']}
OVERALL THREAT LEVEL: {analysis['overall_threat_level']}
THREAT SCORE: {analysis['threat_score']}/10
TOTAL DETECTIONS: {analysis['total_detections']}

THREAT BREAKDOWN:
"""
        for level, count in analysis['threat_breakdown'].items():
            report += f" {level}: {count}\n"
        
        report += "\nDETECTED OBJECTS:\n"
        for obj_data in analysis['detected_objects']:
            report += f" {obj_data['object']} ({obj_data['threat_level']}) - Confidence: {obj_data['confidence']}%\n"
            report += f"  {obj_data['description']}\n"
        
        report += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(analysis['recommendations'], 1):
            report += f"{i}. {rec}\n"
        
        report += "\nSAFETY PROTOCOLS:\n"
        for i, protocol in enumerate(analysis['safety_protocols'], 1):
            report += f"{i}. {protocol}\n"
        
        report += f"\n{'='*50}"
        report += f"\nThis analysis is AI-generated and should be used as a guide.\nAlways use your training and judgment in the field."
        
        return report

# Example usage (for testing purposes)
def test_computer_vision():
    analyzer = ComputerVisionAnalyzer()
    
    print("Sign3T Computer Vision Test")
    print("=" * 50)
    
    # Test 1: Basic object detection
    print("\n1. Testing Object Detection...")
    detections = analyzer._simulate_object_detection("scene.jpg")
    print(f"   Detected {len(detections)} objects:")
    for det in detections:
        threat_info = analyzer.threat_objects.get(det['object'])
        level = threat_info['level'] if threat_info else 'UNKNOWN'
        print(f"   - {det['object']} ({level}) - {det['confidence']:.1%}")

    # Test 2: Full analysis
    print("\n2. Testing Full Analysis...")
    analysis = analyzer.analyze_surveillance_feed("scene.jpg")
    print(f"   Overall Threat Level: {analysis['overall_threat_level']}")
    print(f"   Threat Score: {analysis['threat_score']}/10")
    print(f"   Total Detections: {analysis['total_detections']}")

    # Test 3: Report generation
    print("\n3. Testing Report Generation...")
    report = analyzer.create_surveillance_report("scene.jpg")
    # print(report) # Uncomment to see full report
    print("   Report generated successfully!")
    
    print("\n" + "=" * 50)
    print("Computer Vision Test Complete!")

if __name__ == "__main__":
    test_computer_vision()
