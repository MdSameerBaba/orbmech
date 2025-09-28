#!/usr/bin/env python3
"""
Test the improved project creation parsing
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectAgent import ProjectAgent

def test_project_creation():
    """Test project creation with the new parsing"""
    print("🧪 Testing Project Creation Parsing\n")
    
    # Test the exact command the user wants to use
    command = 'create project "NEXUS Demo App" for testing complete GitHub integration, deadline next month, web app'
    print(f"Command: {command}")
    
    result = ProjectAgent(command)
    print(f"Result: {result}")

if __name__ == "__main__":
    test_project_creation()