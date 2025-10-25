# Sign3T Computer Vision Integration Guide

This guide explains how to use the newly integrated computer vision capabilities within the Sign3T AI Threat Assessment system.

## Overview

The `src/computer_vision.py` module provides functionalities for:
- **Object Detection**: Identifying key objects like weapons, people, vehicles, and suspicious activities in images.
- **Threat Classification**: Assessing the threat level based on visual cues.
- **Recommendation Generation**: Providing AI-driven recommendations and safety protocols.
- **Surveillance Reporting**: Generating comprehensive reports from image analysis.

This module is integrated with `src/simulation.py` to enhance the simulated surveillance feeds with AI-powered visual intelligence.

## Installation

To use the computer vision features, ensure you have the necessary dependencies installed:

```bash
cd /path/to/your/sign3t
source venv/bin/activate
pip install opencv-python pillow
```

These packages are already included in `requirements.txt`, so a `pip install -r requirements.txt` should suffice.

## Core Components

### `src/computer_vision.py`

This file contains the `ComputerVisionAnalyzer` class, which is responsible for:

-   `_simulate_object_detection(image_path: str)`: (Internal) Simulates object detection. In a real-world scenario, this would be replaced by a robust computer vision model (e.g., YOLO, Faster R-CNN). It returns a list of dictionaries, each containing a detected object and a confidence score.
-   `analyze_surveillance_feed(image_path: str)`: The main method for analyzing an image. It calls the simulated object detection and then processes the results to determine an `overall_threat_level`, `threat_score`, and generates `recommendations` and `safety_protocols`.
-   `create_surveillance_report(image_path: str)`: Formats the analysis results into a human-readable surveillance report.

### `src/simulation.py`

The `SurveillanceSimulator` class in this file has been updated to include:

-   `self.computer_vision = ComputerVisionAnalyzer()`: An instance of the `ComputerVisionAnalyzer` for performing visual analysis.
-   `analyze_surveillance_feed_with_cv(self, image_path: str)`: A new method that leverages the `ComputerVisionAnalyzer` to process an image and integrate its findings into the simulation's context, adding `simulation_data` metadata.

## How to Use

### 1. Basic Computer Vision Analysis

You can directly use the `ComputerVisionAnalyzer` for image analysis:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from computer_vision import ComputerVisionAnalyzer

analyzer = ComputerVisionAnalyzer()
image_path = "path/to/your/image.jpg" # Replace with a real image path if you have one, or use a dummy name

# Get a comprehensive analysis of the image
analysis_results = analyzer.analyze_surveillance_feed(image_path)
print("Overall Threat Level:", analysis_results['overall_threat_level'])
print("Detected Objects:", [obj['object'] for obj in analysis_results['detected_objects']])

# Generate a formatted report
report = analyzer.create_surveillance_report(image_path)
print(report)
```

### 2. Integration with Surveillance Simulation

The `SurveillanceSimulator` can now use computer vision to enhance its simulated feeds:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simulation import surveillance_simulator

image_path = "path/to/your/image.jpg" # Dummy image path for simulation

# Analyze a simulated surveillance feed using the integrated CV
cv_enhanced_analysis = surveillance_simulator.analyze_surveillance_feed_with_cv(image_path)

print("AI Confidence from Simulation:", cv_enhanced_analysis['simulation_data']['ai_confidence'])
print("Recommended Response:", cv_enhanced_analysis['simulation_data']['recommended_response'])
print("Visual Detections:", [obj['object'] for obj in cv_enhanced_analysis['detected_objects']])
```

### 3. Running the Comprehensive Example

A dedicated example script `computer_vision_example.py` demonstrates various aspects of the computer vision integration:

```bash
cd /path/to/your/sign3t
source venv/bin/activate
python computer_vision_example.py
```

This script will show:
-   Basic object detection results.
-   Comprehensive threat analysis with scores and breakdowns.
-   AI-generated recommendations and safety protocols.
-   A full surveillance report.
-   How the `SurveillanceSimulator` integrates CV analysis.
-   Simulated threat scenarios (Active Shooter, Domestic Violence, etc.).

## Threat Scenarios Supported

The dummy computer vision logic is designed to simulate detection for various scenarios:

-   **Active Shooter**: Detects `weapon`, `multiple individuals`, `agitated behavior`.
-   **Domestic Violence**: Detects `weapon`, `agitated behavior`, `person`.
-   **Mental Health Crisis**: Detects `person`, `agitated behavior`.
-   **Routine Patrol**: Detects `person`, `vehicle`.

## Future Enhancements

-   Replace `_simulate_object_detection` with a real-time, pre-trained computer vision model (e.g., YOLOv8, Detectron2).
-   Integrate with live video streams from drones or body cameras.
-   Implement facial recognition for known individuals (with privacy safeguards).
-   Develop advanced behavior analysis for more nuanced threat detection.

This guide should help you understand and utilize the computer vision capabilities within your Sign3T project!
