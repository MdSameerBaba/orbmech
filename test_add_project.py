#!/usr/bin/env python3
"""
Test the updated project creation functionality
"""

import sys
sys.path.append('.')
sys.path.append('Backend')
sys.path.append('Backend/Agents')

from Backend.Agents.ProjectAgent import ProjectAgent

def test_add_project():
    """Test the add project command"""
    
    print("🧪 Testing 'add project' command...\n")
    
    # Test the exact command the user used
    command = 'add project "NEXUS Test Project" with deadline "2025-12-01" type "software_development"'
    print(f"Command: {command}")
    
    result = ProjectAgent(command)
    print(f"Result: {result}\n")
    
    # Check if project was created by testing show projects
    print("🔍 Checking if project was created...")
    result2 = ProjectAgent("show projects")
    print(f"Projects: {result2}")

if __name__ == "__main__":
    test_add_project()