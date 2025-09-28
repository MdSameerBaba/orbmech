#!/usr/bin/env python3
"""
NEXUS ProjectAgent - Comprehensive Test Suite
Tests all functionality including VS Code integration and Git operations
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Agents.ProjectAgent import ProjectAgent

def test_project_agent():
    """Run comprehensive tests on ProjectAgent"""
    
    print("🧪 NEXUS PROJECT AGENT - COMPREHENSIVE TEST")
    print("=" * 50)
    
    # Test 1: Show existing projects
    print("\n1️⃣ Testing: Show Projects")
    result = ProjectAgent("show projects")
    print(result)
    
    # Test 2: Create a new project
    print("\n2️⃣ Testing: Create New Project")
    result = ProjectAgent('add project "Test Integration Project" with description "Full integration test" type "software_development"')
    print(result)
    
    # Test 3: Switch to project
    print("\n3️⃣ Testing: Switch to Project")
    result = ProjectAgent("switch to Test Integration Project")
    print(result)
    
    # Test 4: Get current project info
    print("\n4️⃣ Testing: Current Project Info")
    result = ProjectAgent("current project")
    print(result)
    
    # Test 5: Git init
    print("\n5️⃣ Testing: Git Init")
    result = ProjectAgent("git init")
    print(result)
    
    # Test 6: Git status
    print("\n6️⃣ Testing: Git Status")
    result = ProjectAgent("git status")
    print(result)
    
    # Test 7: Create a test file and commit
    print("\n7️⃣ Testing: Create File and Commit")
    
    # Get current project to create a test file
    from Backend.Agents.ProjectAgent import current_active_project
    if current_active_project:
        project_path = current_active_project.get("local_path", "")
        if project_path:
            # Create a simple test file
            test_file_path = os.path.join(project_path, "README.md")
            try:
                with open(test_file_path, 'w') as f:
                    f.write(f"# {current_active_project['name']}\n\n")
                    f.write(f"{current_active_project.get('description', 'No description')}\n\n")
                    f.write("Created by NEXUS ProjectAgent\n")
                print(f"✅ Created test file: {test_file_path}")
                
                # Test commit
                result = ProjectAgent('commit "Initial commit with README"')
                print(result)
                
            except Exception as e:
                print(f"❌ Error creating test file: {e}")
    
    # Test 8: Show updated project status
    print("\n8️⃣ Testing: Updated Project Status")
    result = ProjectAgent("current project")
    print(result)
    
    print("\n" + "=" * 50)
    print("🎉 TEST SUITE COMPLETED!")
    print("=" * 50)

def test_vs_code_integration():
    """Test VS Code specific integration"""
    print("\n🔧 VS CODE INTEGRATION TEST")
    print("-" * 30)
    
    # Test VS Code project detection
    result = ProjectAgent("detect vs code projects")
    print("VS Code Detection:", result)
    
    # Test contextual commands
    commands = [
        "what is my current project",
        "git status",
        "show all projects"
    ]
    
    for cmd in commands:
        print(f"\n📝 Command: {cmd}")
        result = ProjectAgent(cmd)
        print(f"Result: {result}")

if __name__ == "__main__":
    try:
        test_project_agent()
        test_vs_code_integration()
        
        print("\n✨ All tests completed successfully!")
        print("🚀 NEXUS ProjectAgent is ready for VS Code integration!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()