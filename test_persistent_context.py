#!/usr/bin/env python3
"""
Test script to verify persistent project context is working
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectAgent import process_query

def test_persistent_context():
    """Test that project context persists between commands"""
    print("🧪 Testing Persistent Project Context\n")
    
    print("1. Creating a test project...")
    result = process_query("create project 'Context Test App' for testing context persistence, deadline tomorrow, web app")
    print(f"Result: {result}\n")
    
    print("2. Checking current project (should be Context Test App)...")
    result = process_query("current project")
    print(f"Result: {result}\n")
    
    print("3. Testing Git status (should use Context Test App path)...")
    result = process_query("git status")
    print(f"Result: {result}\n")
    
    print("4. Switching to another project if available...")
    result = process_query("list projects")
    print(f"Projects: {result}\n")
    
    print("5. Testing Git status again (should still use correct context)...")
    result = process_query("git status")
    print(f"Result: {result}\n")

if __name__ == "__main__":
    test_persistent_context()