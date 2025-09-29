#!/usr/bin/env python3
"""
Comprehensive AI Project Generator Test Suite
Tests multiple project types and requirements
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectMode.AIProjectManager import AIProjectManager

def test_multiple_project_types():
    """Test AI Project Generator with different project types"""
    print("🧪 Comprehensive AI Project Generator Test Suite")
    print("=" * 60)
    
    manager = AIProjectManager()
    
    test_cases = [
        "build vue.js ecommerce app with stripe payments and product catalog",
        "create python flask api with jwt authentication and postgresql database",
        "make node.js chat application with socket.io and mongodb",
        "develop angular dashboard with charts and user management",
        "build react native mobile app with push notifications"
    ]
    
    results = []
    
    for i, requirements in enumerate(test_cases, 1):
        print(f"\\n🎯 Test {i}: {requirements}")
        print("-" * 50)
        
        result = manager.create_ai_project(requirements)
        
        if result["success"]:
            print(f"✅ SUCCESS! Project '{result['project_name']}' generated!")
            print(f"   📁 Location: {result['project_path']}")
            print(f"   🛠️  Tech Stack: {result['tech_stack']}")
            print(f"   ⚡ Features: {result['features']}")
            print(f"   📄 Files: {result['files_generated']}")
            results.append({"status": "SUCCESS", "project": result['project_name']})
        else:
            print(f"❌ FAILED: {result['error']}")
            results.append({"status": "FAILED", "error": result['error']})
    
    print(f"\\n📊 FINAL RESULTS:")
    print("=" * 60)
    successful = sum(1 for r in results if r["status"] == "SUCCESS")
    total = len(results)
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    for i, result in enumerate(results, 1):
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        if result["status"] == "SUCCESS":
            print(f"   {status_icon} Test {i}: {result['project']}")
        else:
            print(f"   {status_icon} Test {i}: {result['error'][:50]}...")
    
    # List all AI projects
    print(f"\\n🗂️  All AI Projects in Database:")
    ai_projects = manager.list_ai_projects()
    for project in ai_projects:
        print(f"   • {project['name']} (ID: {project['id']}) - {project['tech_stack']}")
    
    return successful == total

if __name__ == "__main__":
    success = test_multiple_project_types()
    if success:
        print(f"\\n🎉 ALL TESTS PASSED! AI Project Generator is working perfectly!")
    else:
        print(f"\\n⚠️  Some tests failed. Check the output above for details.")