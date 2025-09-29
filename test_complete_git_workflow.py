import sys
import os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Backend.Agents.GitIntegration import handle_git_command

def test_complete_git_workflow():
    """Test the complete git workflow with enhanced remote add"""
    print("🧪 Testing Complete Enhanced Git Workflow")
    print("=" * 60)
    
    # Create a test project directory
    test_project_path = r"C:\Users\mdsam\OneDrive\Desktop\orbmech\test_git_project"
    
    # Clean up if exists
    if os.path.exists(test_project_path):
        shutil.rmtree(test_project_path)
    
    # Create test project
    os.makedirs(test_project_path, exist_ok=True)
    
    # Create a simple test file
    with open(os.path.join(test_project_path, "README.md"), "w") as f:
        f.write("# Test Git Project\n\nThis is a test project for enhanced Git integration.")
    
    with open(os.path.join(test_project_path, "app.py"), "w") as f:
        f.write("print('Hello Git Integration!')")
    
    # Test project data
    project_data = {
        "name": "test-git-project",
        "local_path": test_project_path,
        "description": "Test project for enhanced Git integration"
    }
    
    print(f"\n📁 Created test project at: {test_project_path}")
    
    # Step 1: Initialize Git
    print("\n1️⃣ Initializing Git repository...")
    success, message = handle_git_command("git init", project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    # Step 2: Check status
    print("\n2️⃣ Checking Git status...")
    success, message = handle_git_command("git status", project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    # Step 3: Add files
    print("\n3️⃣ Adding files to staging...")
    success, message = handle_git_command("git add .", project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    # Step 4: Commit
    print("\n4️⃣ Committing changes...")
    success, message = handle_git_command('git commit "Initial commit for enhanced Git integration test"', project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    # Step 5: Test enhanced git remote add (this will fail without GitHub auth, but we can see the logic)
    print("\n5️⃣ Testing enhanced git remote add...")
    success, message = handle_git_command("git remote add", project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    # Step 6: Check status again
    print("\n6️⃣ Final status check...")
    success, message = handle_git_command("git status", project_data)
    print(f"   ✅ Success: {success}")
    print(f"   📄 Message: {message}")
    
    print("\n" + "=" * 60)
    print("✅ Complete Git workflow test finished!")
    print(f"📂 Test project remains at: {test_project_path}")

if __name__ == "__main__":
    test_complete_git_workflow()