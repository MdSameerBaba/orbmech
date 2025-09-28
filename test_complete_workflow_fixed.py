#!/usr/bin/env python3
"""
Complete test for NEXUS Project Context Persistence
This tests the end-to-end workflow that was failing for the user
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectAgent import process_query
from Backend.ProjectContext import load_current_project_context, get_current_project_path

def test_complete_workflow():
    """Test the complete workflow: create project -> Git commands"""
    print("🧪 NEXUS Project Context Persistence Test")
    print("=" * 50)
    
    print("\n1️⃣ CREATING NEW PROJECT...")
    result = process_query("create project 'Context Persistence Test' for testing project context, deadline next week, web app")
    print(f"✅ Create Result: {result}")
    
    print("\n2️⃣ CHECKING CURRENT PROJECT CONTEXT...")
    current_project = load_current_project_context()
    if current_project:
        print(f"✅ Loaded Project: {current_project['name']} (ID: {current_project['id']})")
        print(f"📁 Project Path: {current_project.get('local_path', 'Not set')}")
    else:
        print("❌ No current project context found!")
        return False
        
    print("\n3️⃣ TESTING PROJECT PATH FUNCTION...")
    project_path = get_current_project_path()
    print(f"📂 Current Project Path: {project_path}")
    
    print("\n4️⃣ TESTING GIT STATUS COMMAND...")
    result = process_query("git status")
    print(f"🔧 Git Status Result: {result}")
    
    print("\n5️⃣ TESTING GIT INIT COMMAND...")
    result = process_query("git init")
    print(f"🔧 Git Init Result: {result}")
    
    print("\n6️⃣ TESTING PROJECT LIST (should show current project marked)...")
    result = process_query("list projects")
    print(f"📋 List Projects Result: {result}")
    
    print("\n7️⃣ CREATING ANOTHER PROJECT TO TEST SWITCHING...")
    result = process_query("create project 'Second Test Project' for testing project switching, deadline next month, mobile app")
    print(f"✅ Second Project Result: {result}")
    
    print("\n8️⃣ CHECKING CONTEXT AFTER NEW PROJECT...")
    current_project = load_current_project_context()
    if current_project:
        print(f"✅ Current Project: {current_project['name']} (ID: {current_project['id']})")
        print(f"📁 Current Path: {current_project.get('local_path', 'Not set')}")
    
    print("\n9️⃣ SWITCHING BACK TO FIRST PROJECT...")
    result = process_query("switch to project 'Context Persistence Test'")
    print(f"🔄 Switch Result: {result}")
    
    print("\n🔟 FINAL GIT STATUS CHECK (should target first project)...")
    result = process_query("git status")
    print(f"🔧 Final Git Status: {result}")
    
    print("\n" + "=" * 50)
    print("🎯 TEST COMPLETE!")
    
    # Verify final state
    final_project = load_current_project_context()
    if final_project and final_project['name'] == 'Context Persistence Test':
        print("✅ SUCCESS: Project context persistence is working correctly!")
        return True
    else:
        print("❌ FAILURE: Project context not persisting properly!")
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)