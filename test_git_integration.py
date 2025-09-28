#!/usr/bin/env python3
"""
Test Git Integration for OrbMech Project Mode
Run this to verify Git commands work properly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Agents.ProjectAgent import ProjectAgent, get_current_project
from Backend.ModeManager import switch_mode

def test_git_integration():
    print("🧪 Testing Git Integration for OrbMech")
    print("=" * 50)
    
    # Switch to project mode
    print("\n1. Switching to project mode...")
    result = switch_mode("project")
    print(f"   Result: {result}")
    
    # Test project commands
    test_commands = [
        "show projects",
        "git status", 
        "save",
        "push",
        "check status",
        "sync"
    ]
    
    print("\n2. Testing Git commands:")
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n   {i}. Testing: '{cmd}'")
        try:
            response = ProjectAgent(cmd)
            print(f"      Response: {response[:100]}...")
        except Exception as e:
            print(f"      Error: {e}")
    
    print("\n✅ Git integration test completed!")
    print("\n💡 To use Git integration:")
    print("   1. Run 'setup github' first")
    print("   2. Create or switch to a project")
    print("   3. Set project path to your VS Code folder")
    print("   4. Use commands like 'save', 'push', 'status'")

if __name__ == "__main__":
    test_git_integration()