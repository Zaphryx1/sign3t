"""
Simulation Module for Sign3T
Simulates drone and camera feeds for enhanced situational awareness
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from computer_vision import ComputerVisionAnalyzer

class CameraType(Enum):
    """Types of surveillance cameras"""
    DRONE = "drone"
    BODY_CAM = "body_cam"
    TRAFFIC_CAM = "traffic_cam"
    SECURITY_CAM = "security_cam"
    HELICOPTER = "helicopter"

class ThreatIndicator(Enum):
    """Visual threat indicators"""
    WEAPON = "weapon"
    SUSPICIOUS_BEHAVIOR = "suspicious_behavior"
    CROWD_GATHERING = "crowd_gathering"
    VEHICLE_ACCIDENT = "vehicle_accident"
    FIRE = "fire"
    MEDICAL_EMERGENCY = "medical_emergency"

@dataclass
class CameraFeed:
    """Camera feed data structure"""
    camera_id: str
    camera_type: CameraType
    location: str
    timestamp: str
    status: str
    video_url: str
    threat_indicators: List[ThreatIndicator]
    confidence_score: float
    metadata: Dict[str, Any]

class SurveillanceSimulator:
    """Simulates surveillance feeds and real-time monitoring"""
    
    def __init__(self):
        self.active_feeds = {}
        self.computer_vision = ComputerVisionAnalyzer()
        self.threat_patterns = {
            "domestic_violence": [
                ThreatIndicator.SUSPICIOUS_BEHAVIOR,
                ThreatIndicator.WEAPON
            ],
            "traffic_accident": [
                ThreatIndicator.VEHICLE_ACCIDENT,
                ThreatIndicator.MEDICAL_EMERGENCY
            ],
            "public_disturbance": [
                ThreatIndicator.CROWD_GATHERING,
                ThreatIndicator.SUSPICIOUS_BEHAVIOR
            ],
            "fire_emergency": [
                ThreatIndicator.FIRE,
                ThreatIndicator.MEDICAL_EMERGENCY
            ]
        }
    
    def generate_drone_feed(self, location: str, incident_type: str = "domestic_violence") -> CameraFeed:
        """Generate simulated drone feed"""
        camera_id = f"drone_{random.randint(1000, 9999)}"
        
        # Generate threat indicators based on incident type
        threat_indicators = self.threat_patterns.get(incident_type, [])
        
        # Add some randomness
        if random.random() > 0.7:
            threat_indicators.append(random.choice(list(ThreatIndicator)))
        
        feed = CameraFeed(
            camera_id=camera_id,
            camera_type=CameraType.DRONE,
            location=location,
            timestamp=datetime.now().isoformat(),
            status="active",
            video_url=f"https://simulation.sign3t.com/feeds/{camera_id}",
            threat_indicators=threat_indicators,
            confidence_score=random.uniform(0.6, 0.95),
            metadata={
                "altitude": random.randint(50, 200),
                "battery_level": random.randint(20, 100),
                "weather_conditions": random.choice(["clear", "cloudy", "rainy"]),
                "visibility": random.choice(["good", "fair", "poor"]),
                "gps_coordinates": {
                    "lat": 31.7619 + random.uniform(-0.01, 0.01),
                    "lng": -106.4850 + random.uniform(-0.01, 0.01)
                }
            }
        )
        
        self.active_feeds[camera_id] = feed
        return feed
    
    def generate_body_cam_feed(self, officer_id: str, location: str) -> CameraFeed:
        """Generate simulated body camera feed"""
        camera_id = f"body_cam_{officer_id}"
        
        feed = CameraFeed(
            camera_id=camera_id,
            camera_type=CameraType.BODY_CAM,
            location=location,
            timestamp=datetime.now().isoformat(),
            status="recording",
            video_url=f"https://simulation.sign3t.com/body_cam/{camera_id}",
            threat_indicators=[],
            confidence_score=1.0,  # Body cam is always reliable
            metadata={
                "officer_id": officer_id,
                "recording_duration": random.randint(5, 120),
                "battery_level": random.randint(30, 100),
                "storage_available": random.randint(10, 100),
                "audio_enabled": True,
                "night_vision": random.choice([True, False])
            }
        )
        
        self.active_feeds[camera_id] = feed
        return feed
    
    def generate_traffic_cam_feed(self, location: str) -> CameraFeed:
        """Generate simulated traffic camera feed"""
        camera_id = f"traffic_cam_{random.randint(100, 999)}"
        
        feed = CameraFeed(
            camera_id=camera_id,
            camera_type=CameraType.TRAFFIC_CAM,
            location=location,
            timestamp=datetime.now().isoformat(),
            status="monitoring",
            video_url=f"https://simulation.sign3t.com/traffic/{camera_id}",
            threat_indicators=[],
            confidence_score=0.9,
            metadata={
                "traffic_flow": random.choice(["light", "moderate", "heavy"]),
                "weather_conditions": random.choice(["clear", "cloudy", "rainy"]),
                "time_of_day": datetime.now().strftime("%H:%M"),
                "road_conditions": random.choice(["dry", "wet", "icy"])
            }
        )
        
        self.active_feeds[camera_id] = feed
        return feed
    
    def analyze_feed_content(self, feed: CameraFeed) -> Dict[str, Any]:
        """Analyze camera feed content for threats"""
        analysis = {
            "feed_id": feed.camera_id,
            "analysis_timestamp": datetime.now().isoformat(),
            "threats_detected": len(feed.threat_indicators),
            "threat_types": [indicator.value for indicator in feed.threat_indicators],
            "confidence": feed.confidence_score,
            "recommendations": [],
            "alerts": []
        }
        
        # Generate recommendations based on threat indicators
        for indicator in feed.threat_indicators:
            if indicator == ThreatIndicator.WEAPON:
                analysis["alerts"].append("WEAPON DETECTED - HIGH PRIORITY")
                analysis["recommendations"].append("Request immediate backup")
                analysis["recommendations"].append("Establish secure perimeter")
            elif indicator == ThreatIndicator.SUSPICIOUS_BEHAVIOR:
                analysis["alerts"].append("Suspicious activity detected")
                analysis["recommendations"].append("Monitor closely")
                analysis["recommendations"].append("Document behavior")
            elif indicator == ThreatIndicator.CROWD_GATHERING:
                analysis["alerts"].append("Crowd gathering detected")
                analysis["recommendations"].append("Assess crowd size and behavior")
                analysis["recommendations"].append("Consider crowd control measures")
            elif indicator == ThreatIndicator.FIRE:
                analysis["alerts"].append("FIRE DETECTED - EMERGENCY")
                analysis["recommendations"].append("Contact fire department")
                analysis["recommendations"].append("Evacuate if necessary")
        
        return analysis
    
    def get_all_active_feeds(self) -> List[CameraFeed]:
        """Get all active camera feeds"""
        return list(self.active_feeds.values())
    
    def get_feeds_by_location(self, location: str) -> List[CameraFeed]:
        """Get camera feeds for specific location"""
        return [feed for feed in self.active_feeds.values() if location.lower() in feed.location.lower()]
    
    def simulate_real_time_updates(self, location: str, duration_minutes: int = 5) -> List[Dict[str, Any]]:
        """Simulate real-time updates from surveillance feeds"""
        updates = []
        
        for minute in range(duration_minutes):
            # Generate random updates
            if random.random() > 0.3:  # 70% chance of update each minute
                update = {
                    "timestamp": (datetime.now() + timedelta(minutes=minute)).isoformat(),
                    "location": location,
                    "update_type": random.choice([
                        "new_threat_detected",
                        "situation_escalated",
                        "backup_arrived",
                        "situation_resolved",
                        "new_individual_spotted"
                    ]),
                    "description": self._generate_update_description(),
                    "priority": random.choice(["low", "medium", "high", "critical"]),
                    "source": random.choice(["drone", "body_cam", "traffic_cam", "officer_report"])
                }
                updates.append(update)
        
        return updates
    
    def _generate_update_description(self) -> str:
        """Generate realistic update descriptions"""
        descriptions = [
            "Subject appears agitated and pacing",
            "Additional individuals approaching scene",
            "Vehicle with tinted windows circling area",
            "Loud shouting heard from inside residence",
            "Subject making threatening gestures",
            "Crowd gathering on street corner",
            "Smoke visible from second floor window",
            "Subject has moved to backyard area",
            "Multiple people exiting building",
            "Emergency vehicle approaching scene"
        ]
        return random.choice(descriptions)
    
    def generate_situational_awareness_report(self, location: str) -> Dict[str, Any]:
        """Generate comprehensive situational awareness report"""
        # Get all feeds for location
        location_feeds = self.get_feeds_by_location(location)
        
        # Analyze each feed
        feed_analyses = []
        for feed in location_feeds:
            analysis = self.analyze_feed_content(feed)
            feed_analyses.append(analysis)
        
        # Generate real-time updates
        real_time_updates = self.simulate_real_time_updates(location, 3)
        
        # Compile comprehensive report
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "location": location,
            "total_feeds": len(location_feeds),
            "active_cameras": [feed.camera_id for feed in location_feeds],
            "threat_summary": {
                "total_threats": sum(analysis["threats_detected"] for analysis in feed_analyses),
                "high_priority_alerts": len([update for update in real_time_updates if update["priority"] == "critical"]),
                "weapons_detected": any("weapon" in analysis["threat_types"] for analysis in feed_analyses)
            },
            "feed_analyses": feed_analyses,
            "real_time_updates": real_time_updates,
            "recommendations": self._generate_situational_recommendations(feed_analyses, real_time_updates)
        }
        
        return report
    
    def _generate_situational_recommendations(self, feed_analyses: List[Dict], updates: List[Dict]) -> List[str]:
        """Generate recommendations based on feed analyses and updates"""
        recommendations = []
        
        # Check for high-priority alerts
        critical_updates = [update for update in updates if update["priority"] == "critical"]
        if critical_updates:
            recommendations.append("CRITICAL: Immediate tactical response required")
            recommendations.append("Request SWAT team deployment")
        
        # Check for weapons
        weapon_detected = any("weapon" in analysis["threat_types"] for analysis in feed_analyses)
        if weapon_detected:
            recommendations.append("Weapons detected - maintain safe distance")
            recommendations.append("Use cover and concealment")
        
        # Check for crowd situations
        crowd_updates = [update for update in updates if "crowd" in update["description"].lower()]
        if crowd_updates:
            recommendations.append("Crowd situation - consider crowd control measures")
            recommendations.append("Monitor for escalation")
        
        # General recommendations
        recommendations.extend([
            "Maintain situational awareness",
            "Document all observations",
            "Communicate with dispatch regularly"
        ])
        
        return recommendations
    
    def analyze_surveillance_feed_with_cv(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze surveillance feed using computer vision
        Returns comprehensive threat analysis
        """
        try:
            # Use computer vision analyzer
            analysis = self.computer_vision.analyze_surveillance_feed(image_path)
            
            # Add simulation-specific metadata
            analysis["simulation_data"] = {
                "camera_type": "surveillance_feed",
                "analysis_timestamp": datetime.now().isoformat(),
                "ai_confidence": analysis.get("threat_score", 0) / 10,
                "recommended_response": self._get_response_recommendation(analysis["overall_threat_level"])
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error in computer vision analysis: {e}")
            return {
                "error": str(e),
                "fallback_analysis": "Manual review required",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_response_recommendation(self, threat_level: str) -> str:
        """Get response recommendation based on threat level"""
        recommendations = {
            "CRITICAL": "Immediate tactical response - SWAT team required",
            "HIGH": "High priority response - backup units needed",
            "MEDIUM": "Standard response - monitor situation",
            "LOW": "Routine patrol - continue monitoring"
        }
        return recommendations.get(threat_level, "Assess situation manually")

# Initialize surveillance simulator
surveillance_simulator = SurveillanceSimulator()

def generate_surveillance_feeds(location: str, incident_type: str = "domestic_violence") -> List[CameraFeed]:
    """Generate surveillance feeds for a location"""
    feeds = []
    
    # Generate drone feed
    drone_feed = surveillance_simulator.generate_drone_feed(location, incident_type)
    feeds.append(drone_feed)
    
    # Generate body cam feed
    body_cam_feed = surveillance_simulator.generate_body_cam_feed("OFFICER_001", location)
    feeds.append(body_cam_feed)
    
    # Generate traffic cam feed
    traffic_cam_feed = surveillance_simulator.generate_traffic_cam_feed(location)
    feeds.append(traffic_cam_feed)
    
    return feeds

def get_situational_awareness(location: str) -> Dict[str, Any]:
    """Get comprehensive situational awareness for a location"""
    return surveillance_simulator.generate_situational_awareness_report(location)
