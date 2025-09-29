#!/usr/bin/env python3
"""
Test NEXUS AI Project Generation Commands
Surface-level user testing
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectAgent import ProjectAgent, is_ai_project_generation_request

def test_command_detection():
    """Test if AI project generation commands are properly detected"""
    print("🧪 Testing AI Project Generation Command Detection")
    print("=" * 60)
    
    test_commands = [
        "create react todo app with authentication",
        "build vue.js ecommerce site with payments", 
        "make python flask api with database",
        "generate angular dashboard with charts",
        "create mobile app with react native",
        "build node.js chat application",
        "create project MyApp",  # Should NOT be detected (traditional)
        "what's the weather like today",  # Should NOT be detected
        "switch to project TestRepo"  # Should NOT be detected
    ]
    
    for cmd in test_commands:
        is_ai_gen = is_ai_project_generation_request(cmd)
        status = "✅ AI GEN" if is_ai_gen else "❌ NOT AI GEN"
        print(f"{status}: {cmd}")
    
    print()

def test_ai_project_generation():
    """Test actual AI project generation through ProjectAgent"""
    print("🚀 Testing AI Project Generation Execution")
    print("=" * 60)
    
    test_command = "create react todo app with drag and drop and authentication"
    print(f"Testing command: {test_command}")
    print("-" * 40)
    
    try:
        result = ProjectAgent(test_command)
        print("✅ SUCCESS!")
        print(result)
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_command_detection()
    print()
    test_ai_project_generation()