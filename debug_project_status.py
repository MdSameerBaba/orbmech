#!/usr/bin/env python3
"""
Debug the project switching issue
"""

import sys
sys.path.append('.')
sys.path.append('Backend')

from Backend.VSCodeIntegration import handle_vscode_integration

def test_current_project_status():
    """Test what project is currently active"""
    
    print("🔍 Debugging Project Status...\n")
    
    # Check current project
    response = handle_vscode_integration("current project")
    print(f"Current Project Status:\n{response}\n")
    
    # Try switching again
    print("🔄 Attempting to switch to NEXUS Test Project...")
    response = handle_vscode_integration("switch to NEXUS Test Project")
    print(f"Switch Response: {response}\n")
    
    # Check status after switch
    response = handle_vscode_integration("current project")
    print(f"Status After Switch:\n{response}")

if __name__ == "__main__":
    test_current_project_status()