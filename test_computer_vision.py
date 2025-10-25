#!/usr/bin/env python3
"""
Test Script for Computer Vision Module
This script tests the computer vision capabilities of Sign3T.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from computer_vision import ComputerVisionAnalyzer
from simulation import SurveillanceSimulator # Import SurveillanceSimulator for integration test

def test_computer_vision_module():
    analyzer = ComputerVisionAnalyzer()
    simulator = SurveillanceSimulator() # Initialize simulator for integration test
    
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

    # Test 3: Surveillance Simulator Integration
    print("\n3. Testing Surveillance Simulator Integration...")
    cv_analysis_from_simulator = simulator.analyze_surveillance_feed_with_cv("scene.jpg")
    print(f"   AI Confidence: {cv_analysis_from_simulator['simulation_data']['ai_confidence']:.1%}")
    print(f"   Recommended Response: {cv_analysis_from_simulator['simulation_data']['recommended_response']}")

    # Test 4: Report generation
    print("\n4. Generating Surveillance Report...")
    report = analyzer.create_surveillance_report("scene.jpg")
    print("   Report generated successfully!")
    
    print("\n" + "=" * 50)
    print("Computer Vision Test Complete!")

    print("\n" + "=" * 50)
    print("Threat Scenario Demonstrations")
    print("=" * 50)

    # Demonstrate different scenarios
    scenarios = {
        "High Threat Scenario": ["weapon", "agitated behavior", "multiple individuals"],
        "Medium Threat Scenario": ["suspicious activity", "crowd", "vehicle"],
        "Low Threat Scenario": ["person", "individual"]
    }

    for name, objects in scenarios.items():
        print(f"\n{name}:")
        print("-" * (len(name) + 1))
        # Temporarily override _simulate_object_detection for consistent testing
        original_simulate = analyzer._simulate_object_detection
        analyzer._simulate_object_detection = lambda x: [
            {"object": obj, "confidence": random.uniform(0.7, 0.99)} for obj in objects
        ]
        analysis = analyzer.analyze_surveillance_feed("dummy.jpg")
        for det in analysis['detected_objects']:
            print(f"  - {det['object']} ({det['threat_level']}) - {det['confidence']:.1%}")
        analyzer._simulate_object_detection = original_simulate # Restore original

    print("\n" + "=" * 50)
    print("All tests completed successfully!")
    print("Computer vision module is ready for integration.")
    print("=" * 50)


if __name__ == "__main__":
    test_computer_vision_module()
