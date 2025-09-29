import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Backend.Agents.ProjectAgent import handle_ai_project_generation, is_ai_project_generation_request
from Backend.Agents.GitIntegration import handle_git_command

def test_fresh_project_and_git_workflow():
    """Generate a fresh project and test complete Git workflow"""
    print("🚀 NEXUS Fresh Project + Enhanced Git Workflow Test")
    print("=" * 60)
    
    # Test project request
    project_request = """Create a modern personal finance tracker web app with the following features:
    - React frontend with TypeScript
    - Node.js Express backend with MongoDB
    - User authentication and registration
    - Expense tracking with categories
    - Budget management system
    - Financial goals tracking
    - Interactive charts for spending analysis
    - Monthly/yearly financial reports
    - Bill reminders and notifications
    
    Make it a complete full-stack application with proper database schema and API endpoints."""
    
    print(f"\n📋 Project Request:")
    print(f"   {project_request[:100]}...")
    
    try:
        # Check if this is an AI project generation request
        print(f"\n1️⃣ Validating AI project generation request...")
        is_ai_request = is_ai_project_generation_request(project_request)
        print(f"   ✅ Is AI Request: {is_ai_request}")
        
        if is_ai_request:
            # Generate the project
            print(f"\n2️⃣ Generating fresh project with NEXUS AI...")
            response = handle_ai_project_generation(project_request)
            
            print(f"   📄 Response: {response[:300]}...")
            
            # Extract project info from response (we'll need to parse it or check the Generated_Projects folder)
            import glob
            import time
            
            # Wait a moment for file creation
            time.sleep(2)
            
            # Find the most recently created project
            projects_pattern = r"Generated_Projects\*"
            project_folders = glob.glob(projects_pattern)
            
            if project_folders:
                # Get the most recent folder
                latest_project = max(project_folders, key=os.path.getctime)
                project_name = os.path.basename(latest_project)
                
                # Create project_data structure for Git integration
                project_data = {
                    'name': project_name,
                    'local_path': latest_project,
                    'description': 'AI Generated Personal Finance Tracker'
                }
                
                success = True
                
                project_name = project_data.get('name', 'personal-finance-tracker')
                project_path = project_data.get('local_path', '')
                
                print(f"\n📁 Generated Project:")
                print(f"   Name: {project_name}")
                print(f"   Path: {project_path}")
                
                # Test Git workflow
                print(f"\n🔧 Testing Enhanced Git Workflow...")
                
                # Step 1: Initialize Git
                print(f"\n3️⃣ Initializing Git repository...")
            success, message = handle_git_command("git init", project_data)
            print(f"   ✅ Success: {success}")
            print(f"   📄 Message: {message[:150]}...")
            
            if success:
                if success:
                    # Step 2: Add files
                    print(f"\n4️⃣ Adding files to Git...")
                    success, message = handle_git_command("git add .", project_data)
                    print(f"   ✅ Success: {success}")
                    print(f"   📄 Message: {message[:150]}...")
                    
                    # Step 3: Commit
                    print(f"\n5️⃣ Committing initial version...")
                    success, message = handle_git_command('git commit "Initial version of personal finance tracker"', project_data)
                    print(f"   ✅ Success: {success}")
                    print(f"   📄 Message: {message[:150]}...")
                    
                    # Step 4: Enhanced remote add (NEW FEATURE)
                    print(f"\n6️⃣ Testing enhanced git remote add...")
                    success, message = handle_git_command("git remote add", project_data)
                    print(f"   ✅ Success: {success}")
                    print(f"   📄 Message: {message[:150]}...")
                    
                    # Step 5: Check final status
                    print(f"\n7️⃣ Final Git status check...")
                success, message = handle_git_command("git status", project_data)
                print(f"   ✅ Success: {success}")
                print(f"   📄 Status: {message[:200]}...")
                
                # Show project structure
                if os.path.exists(project_path):
                    print(f"\n📂 Generated Project Structure:")
                    for root, dirs, files in os.walk(project_path):
                        # Limit depth to avoid too much output
                        level = root.replace(project_path, '').count(os.sep)
                        if level < 3:
                            indent = ' ' * 2 * level
                            folder_name = os.path.basename(root)
                            if folder_name:
                                print(f"{indent}{folder_name}/")
                            subindent = ' ' * 2 * (level + 1)
                            for file in files[:5]:  # Show max 5 files per folder
                                print(f"{subindent}{file}")
                            if len(files) > 5:
                                print(f"{subindent}... and {len(files) - 5} more files")
            else:
                print(f"❌ No project folders found in Generated_Projects")
        else:
            print(f"❌ Not recognized as AI project generation request")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n" + "=" * 60)
    print(f"✅ Fresh Project + Git Workflow Test Complete!")

if __name__ == "__main__":
    test_fresh_project_and_git_workflow()