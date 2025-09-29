#!/usr/bin/env python3
"""
Test the Requirements Analyzer
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectMode.RequirementsAnalyzer import RequirementsAnalyzer
import json

def test_requirements_analyzer():
    """Test the requirements analyzer with various inputs"""
    analyzer = RequirementsAnalyzer()
    
    test_cases = [
        "create react todo app with drag and drop and user authentication",
        "build fullstack ecommerce website with payment integration and admin dashboard",
        "create mobile app for fitness tracking with charts and social sharing",
        "build portfolio website with blog and contact form",
        "create nodejs api for social media with real-time chat"
    ]
    
    print("🧪 Testing Requirements Analyzer\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case}")
        print("-" * 60)
        
        requirements = analyzer.analyze(test_case)
        
        print(f"📝 Project Name: {requirements.name}")
        print(f"🛠️  Tech Stack: {requirements.tech_stack}")
        print(f"⚡ Features: {requirements.features}")
        print(f"🧩 Components: {requirements.components[:5]}...")  # Show first 5
        print(f"📄 Pages: {requirements.pages}")
        print(f"📦 Dependencies: {requirements.dependencies[:5]}...")  # Show first 5
        print(f"🔐 Authentication: {requirements.authentication}")
        
        recommendations = analyzer.get_recommendations(requirements)
        print(f"💡 Additional Features: {recommendations['additional_features'][:3]}")
        
        print("\n")

if __name__ == "__main__":
    test_requirements_analyzer()