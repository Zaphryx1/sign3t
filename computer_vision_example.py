#!/usr/bin/env python3
"""
Comprehensive Example for Computer Vision Module Integration in Sign3T
This script demonstrates how to use the computer vision capabilities for threat assessment.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from computer_vision import ComputerVisionAnalyzer
from simulation import surveillance_simulator # Import the initialized simulator

def run_computer_vision_demo():
    analyzer = ComputerVisionAnalyzer()
    
    print("Sign3T Computer Vision Demonstration")
    print("=" * 60)

    # --- 1. Basic Object Detection ---
    print("\n1. BASIC OBJECT DETECTION")
    print("-" * 30)
    image_path = "surveillance_feed.jpg" # Dummy image path
    
    # Simulate object detection directly
    detected_objects_raw = analyzer._simulate_object_detection(image_path)
    print("Analyzing surveillance feed...")
    
    # Process raw detections to get threat info
    threat_detections = []
    for obj_data in detected_objects_raw:
        obj_name = obj_data["object"]
        confidence = obj_data["confidence"]
        threat_info = analyzer.threat_objects.get(obj_name)
        if threat_info:
            threat_level = threat_info["level"]
            threat_detections.append({
                "object": obj_name,
                "threat_level": threat_level,
                "confidence": round(confidence * 100, 1),
                "description": f"Detected {obj_name} with {threat_level} threat level"
            })
    
    print(f"Detected {len(threat_detections)} objects:")
    for det in threat_detections:
        print(f"   {det['object']}")
        print(f"    Threat Level: {det['threat_level']}")
        print(f"    Confidence: {det['confidence']:.1%}")
        print(f"    Description: {det['description']}\n")


    # --- 2. Comprehensive Threat Analysis ---
    print("\n2. COMPREHENSIVE THREAT ANALYSIS")
    print("-" * 40)
    analysis = analyzer.analyze_surveillance_feed(image_path)
    
    print(f"Overall Threat Level: {analysis['overall_threat_level']}")
    print(f"Threat Score: {analysis['threat_score']}/10")
    print(f"Total Detections: {analysis['total_detections']}")
    print(f"Analysis Timestamp: {analysis['timestamp']}\n")
    
    print("Threat Breakdown:")
    for level, count in analysis['threat_breakdown'].items():
        print(f"   {level}: {count}")

    # --- 3. Recommendations & Safety Protocols ---
    print("\n3. RECOMMENDATIONS & SAFETY PROTOCOLS")
    print("-" * 45)
    print("AI-Generated Recommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\nSafety Protocols:")
    for i, protocol in enumerate(analysis['safety_protocols'], 1):
        print(f"  {i}. {protocol}")

    # --- 4. Complete Surveillance Report ---
    print("\n4. COMPLETE SURVEILLANCE REPORT")
    print("-" * 40)
    report = analyzer.create_surveillance_report(image_path)
    print(report)

    # --- 5. Surveillance Simulator Integration ---
    print("\n5. SURVEILLANCE SIMULATOR INTEGRATION")
    print("-" * 45)
    cv_analysis_from_simulator = surveillance_simulator.analyze_surveillance_feed_with_cv(image_path)
    print(f"Camera Type: {cv_analysis_from_simulator['simulation_data']['camera_type']}")
    print(f"AI Confidence: {cv_analysis_from_simulator['simulation_data']['ai_confidence']:.1%}")
    print(f"Recommended Response: {cv_analysis_from_simulator['simulation_data']['recommended_response']}")

    print("\n" + "=" * 60)
    print("THREAT SCENARIO DEMONSTRATIONS")
    print("=" * 60)

    # Demonstrate different scenarios using the simulator's CV integration
    scenario_descriptions = {
        "Active Shooter Scenario": "Multiple individuals with weapons in public area",
        "Domestic Violence Scenario": "Agitated individual with potential weapon in residential area",
        "Mental Health Crisis Scenario": "Individual in distress, no weapons visible",
        "Routine Patrol Scenario": "Normal activity, no threats detected"
    }

    for name, desc in scenario_descriptions.items():
        print(f"\n{name}")
        print("-" * (len(name) + 1))
        print(f"Description: {desc}")
        print(f"Expected Objects: {', '.join(analyzer._simulate_object_detection('dummy.jpg')[0]['object'] for _ in range(random.randint(1,3)))}") # Dummy expected objects
        print(f"Expected Threat Level: {random.choice(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'])}") # Dummy expected level
        print("Simulated Analysis Results:")
        # Here you would call the actual CV analysis with a specific image for the scenario
        # For this demo, we'll just print a placeholder
        print("   AI would detect relevant objects")
        print("   Threat level would be assessed")
        print("   Appropriate recommendations generated")
        print("   Safety protocols activated")

    print("\n" + "=" * 60)
    print("INTEGRATION WITH SIGN3T SYSTEM")
    print("=" * 60)
    print("\nTo integrate computer vision with your Sign3T system:")
    print("\n1. Import the modules:")
    print("   from computer_vision import ComputerVisionAnalyzer")
    print("   from simulation import surveillance_simulator")
    print("\n2. Analyze surveillance feeds:")
    print("   analyzer = ComputerVisionAnalyzer()")
    print("   analysis = analyzer.analyze_surveillance_feed(\"image.jpg\")")
    print("\n3. Get threat assessment:")
    print("   threat_level = analysis['overall_threat_level']")
    print("   threat_score = analysis['threat_score']")
    print("\n4. Generate officer briefing:")
    print("   report = analyzer.create_surveillance_report(\"image.jpg\")")
    print("\n5. Integrate with surveillance simulation:")
    print("   cv_analysis = surveillance_simulator.analyze_surveillance_feed_with_cv(\"image.jpg\")")
    print("\n6. Use in threat assessment:")
    print("   # Combine with other data sources")
    print("   # Update threat assessment with visual intelligence")
    print("   # Generate comprehensive officer briefing")

    print("\n" + "=" * 60)
    print("COMPUTER VISION DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("The computer vision module is ready for integration")
    print("with your Sign3T threat assessment system!")
    print("=" * 60)


if __name__ == "__main__":
    run_computer_vision_demo()
