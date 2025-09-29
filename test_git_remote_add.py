import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Backend.Agents.GitIntegration import handle_git_command

def test_git_remote_add():
    """Test the new simplified git remote add command"""
    print("🧪 Testing Enhanced Git Remote Add Command")
    print("=" * 50)
    
    # Test project data (simulating React Todo project)
    project_data = {
        "name": "react-todo-app",
        "local_path": r"C:\Users\mdsam\OneDrive\Desktop\orbmech\Generated_Projects\react-todo-app",
        "description": "A React-based todo application"
    }
    
    # Test 1: git remote add command
    print("\n1. Testing 'git remote add' command...")
    success, message = handle_git_command("git remote add", project_data)
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    
    # Test 2: Alternative phrasing
    print("\n2. Testing 'add remote' command...")
    success, message = handle_git_command("add remote", project_data)
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    
    # Test 3: Help command to see all available commands
    print("\n3. Testing help (unknown command)...")
    success, message = handle_git_command("help", project_data)
    print(f"   Result: {success}")
    print(f"   Message: {message}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    test_git_remote_add()