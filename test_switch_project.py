#!/usr/bin/env python3
"""
Test switching to NEXUS Test Project
"""

import sys
sys.path.append('.')
sys.path.append('Backend')

from Backend.VSCodeIntegration import handle_vscode_integration

def test_switch_project():
    """Test switching to NEXUS Test Project"""
    
    print("🧪 Testing project switching...\n")
    
    # Test switching to NEXUS Test Project
    command = "switch to NEXUS Test Project"
    print(f"Command: {command}")
    
    result = handle_vscode_integration(command)
    print(f"Result: {result}\n")
    
    # Check current project status
    print("🔍 Checking current project status...")
    result2 = handle_vscode_integration("current project")
    print(f"Status: {result2}")

if __name__ == "__main__":
    test_switch_project()