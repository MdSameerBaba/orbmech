#!/usr/bin/env python3
"""
Test the complete AI Project Generator
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Agents.ProjectMode.AIProjectManager import AIProjectManager

def test_ai_project_generator():
    """Test the complete AI project generation workflow"""
    print("🤖 Testing AI Project Generator\n")
    
    # Initialize the AI Project Manager
    manager = AIProjectManager()
    
    # Test case: Create a React todo app
    requirements = "create react todo app with drag and drop, user authentication, and dark mode"
    
    print(f"🎯 Testing: {requirements}")
    print("=" * 80)
    
    # Generate the project
    result = manager.create_ai_project(requirements)
    
    if result["success"]:
        print(f"✅ SUCCESS! Project '{result['project_name']}' generated!")
        print(f"📁 Location: {result['project_path']}")
        print(f"🆔 Project ID: {result['project_id']}")
        print(f"🛠️  Tech Stack: {result['tech_stack']}")
        print(f"⚡ Features: {result['features']}")
        print(f"📄 Files Generated: {result['files_generated']}")
        
        print(f"\\n🚀 Setup Instructions:")
        for i, instruction in enumerate(result['setup_instructions'], 1):
            print(f"   {i}. {instruction}")
        
        print(f"\\n💡 Recommendations:")
        for category, items in result['recommendations'].items():
            if items:
                print(f"   {category.replace('_', ' ').title()}: {', '.join(items[:3])}")
        
        # Test listing AI projects
        print(f"\\n📋 All AI Projects:")
        ai_projects = manager.list_ai_projects()
        for project in ai_projects:
            print(f"   • {project['name']} (ID: {project['id']}) - {project['tech_stack']}")
        
    else:
        print(f"❌ FAILED: {result['error']}")

if __name__ == "__main__":
    test_ai_project_generator()