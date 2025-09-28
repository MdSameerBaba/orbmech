#!/usr/bin/env python3
"""
Quick Git workflow test for NEXUS Feature Demo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Agents.ProjectAgent import ProjectAgent

def test_git_workflow():
    print("=== COMPLETE GIT WORKFLOW TEST ===")
    
    print("1. Switch to project:")
    result = ProjectAgent('switch to NEXUS Feature Demo')
    print(result)
    
    print("\n2. Git init:")
    result = ProjectAgent('git init')
    print(result)
    
    print("\n3. Git status:")
    result = ProjectAgent('git status')
    print(result)
    
    print("\n4. Git commit:")
    result = ProjectAgent('commit "Complete NEXUS feature demonstration"')
    print(result)
    
    print("\n5. Current project status:")
    result = ProjectAgent('current project')
    print(result)

if __name__ == "__main__":
    test_git_workflow()