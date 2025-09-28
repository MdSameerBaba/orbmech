#!/usr/bin/env python3
"""
Test VS Code Integration Features for NEXUS Project Mode
"""

import sys
sys.path.append('.')
sys.path.append('Backend')

from Backend.VSCodeIntegration import handle_vscode_integration, vscode_manager

def test_vscode_integration():
    """Test the new VS Code integration features"""
    
    print("🧪 Testing VS Code Integration Features\n")
    
    # Test 1: Detect VS Code projects
    print("1️⃣ Testing project detection...")
    response = handle_vscode_integration("detect projects")
    print(f"Response: {response}\n")
    
    # Test 2: Project status without active project
    print("2️⃣ Testing project status (no active project)...")
    response = handle_vscode_integration("current project")
    print(f"Response: {response}\n")
    
    # Test 3: Switch to TestRepo project
    print("3️⃣ Testing project switching...")
    response = handle_vscode_integration("switch to TestRepo")
    print(f"Response: {response}\n")
    
    # Test 4: Project status with active project
    print("4️⃣ Testing project status (with active project)...")
    response = handle_vscode_integration("current project")
    print(f"Response: {response}\n")
    
    # Test 5: Git help commands
    print("5️⃣ Testing git help...")
    response = handle_vscode_integration("git help")
    print(f"Response: {response}\n")
    
    # Test 6: Git status (contextual)
    print("6️⃣ Testing contextual git status...")
    response = handle_vscode_integration("git status")
    print(f"Response: {response}\n")
    
    # Test 7: Try switching to different project
    print("7️⃣ Testing switch to MyNewApp...")
    response = handle_vscode_integration("switch to MyNewApp")
    print(f"Response: {response}\n")
    
    print("✅ VS Code Integration tests completed!")

if __name__ == "__main__":
    test_vscode_integration()