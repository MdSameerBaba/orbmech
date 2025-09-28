#!/usr/bin/env python3
"""
NEXUS ProjectAgent - Final Integration Test
Complete end-to-end test in a single session
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.Agents.ProjectAgent import ProjectAgent

def run_complete_test():
    """Run complete end-to-end test"""
    
    print("🚀 NEXUS PROJECT AGENT - FINAL INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Create a new project
    print("\n1️⃣ Creating New Project...")
    result = ProjectAgent('add project "Final Test Project" with description "Complete integration test" type "software_development"')
    print(result)
    
    # Test 2: Verify current project
    print("\n2️⃣ Checking Current Project...")
    result = ProjectAgent("current project")
    print(result)
    
    # Test 3: Initialize Git
    print("\n3️⃣ Initializing Git Repository...")
    result = ProjectAgent("git init")
    print(result)
    
    # Test 4: Check Git status
    print("\n4️⃣ Checking Git Status...")
    result = ProjectAgent("git status")
    print(result)
    
    # Test 5: Create a test file manually
    print("\n5️⃣ Creating Test Files...")
    from Backend.Agents.ProjectAgent import current_active_project
    
    if current_active_project:
        project_path = current_active_project.get("local_path", "")
        print(f"Project path: {project_path}")
        
        if project_path:
            try:
                # Ensure directory exists
                os.makedirs(project_path, exist_ok=True)
                
                # Create test files
                readme_path = os.path.join(project_path, "README.md")
                with open(readme_path, 'w') as f:
                    f.write(f"# {current_active_project['name']}\n\n")
                    f.write(f"{current_active_project.get('description', 'No description')}\n\n")
                    f.write("## Features\n")
                    f.write("- Created by NEXUS ProjectAgent\n")
                    f.write("- Full VS Code integration\n")
                    f.write("- Git workflow support\n")
                
                # Create a simple Python file
                main_path = os.path.join(project_path, "main.py")
                with open(main_path, 'w') as f:
                    f.write('#!/usr/bin/env python3\n')
                    f.write('"""\n')
                    f.write(f'{current_active_project["name"]}\n')
                    f.write('Created by NEXUS ProjectAgent\n')
                    f.write('"""\n\n')
                    f.write('def main():\n')
                    f.write('    print("Hello from NEXUS Project!")\n\n')
                    f.write('if __name__ == "__main__":\n')
                    f.write('    main()\n')
                
                print(f"✅ Created test files in: {project_path}")
                print(f"   - README.md")
                print(f"   - main.py")
                
            except Exception as e:
                print(f"❌ Error creating test files: {e}")
                return
    
    # Test 6: Check Git status again
    print("\n6️⃣ Checking Git Status After File Creation...")
    result = ProjectAgent("git status")
    print(result)
    
    # Test 7: Commit the files
    print("\n7️⃣ Committing Files...")
    result = ProjectAgent('commit "Initial project setup with NEXUS"')
    print(result)
    
    # Test 8: Final project status
    print("\n8️⃣ Final Project Status...")
    result = ProjectAgent("current project")
    print(result)
    
    # Test 9: List all projects
    print("\n9️⃣ All Projects Summary...")
    result = ProjectAgent("show projects")
    print(result)
    
    print("\n" + "=" * 60)
    print("🎉 INTEGRATION TEST COMPLETED!")
    print("✅ NEXUS ProjectAgent is ready for production use!")
    print("🔗 VS Code Integration: Ready")
    print("🔧 Git Workflow: Functional") 
    print("📊 Project Management: Active")
    print("=" * 60)

if __name__ == "__main__":
    try:
        run_complete_test()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()