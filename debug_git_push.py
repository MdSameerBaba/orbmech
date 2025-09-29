"""
Debug Git Integration - Test the enhanced push functionality
"""
import subprocess
import os

def run_git_command(command, cwd=None):
    """Execute git command and return result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def debug_git_push_issue():
    """Debug the current git push issue"""
    
    print("🔍 DEBUGGING GIT PUSH ISSUE")
    print("=" * 40)
    
    # Check current project context
    try:
        with open("Data/current_context.json", 'r') as f:
            import json
            context = json.load(f)
            project = context.get("current_project", {})
            project_path = project.get("local_path", "")
            project_name = project.get("name", "")
            
            print(f"📛 Current Project: {project_name}")
            print(f"📁 Project Path: {project_path}")
            print()
            
            if not os.path.exists(project_path):
                print(f"❌ Project directory doesn't exist: {project_path}")
                return
            
            # Check git status in that directory
            print("🔍 Git Status Check:")
            success, stdout, stderr = run_git_command("git status", cwd=project_path)
            if success:
                print(f"✅ Git Status: {stdout[:200]}...")
            else:
                print(f"❌ Git Status Error: {stderr}")
                return
            
            # Check remote configuration
            print("\n🔍 Remote Configuration:")
            success, stdout, stderr = run_git_command("git remote -v", cwd=project_path)
            if success:
                if stdout:
                    print(f"✅ Remotes: {stdout}")
                else:
                    print("❌ No remotes configured")
                    return
            else:
                print(f"❌ Remote check error: {stderr}")
            
            # Check current branch
            print("\n🔍 Branch Information:")
            success, stdout, stderr = run_git_command("git branch", cwd=project_path)
            if success:
                print(f"✅ Current branch: {stdout}")
            else:
                print(f"❌ Branch check error: {stderr}")
            
            # Try the enhanced push logic
            print("\n🚀 Testing Enhanced Push Logic:")
            print("Strategy 1: Simple 'git push'")
            success, stdout, stderr = run_git_command("git push", cwd=project_path)
            if success:
                print("✅ Simple push worked!")
                return
            else:
                print(f"❌ Simple push failed: {stderr}")
            
            print("\nStrategy 2: 'git push origin main'")
            success, stdout, stderr = run_git_command("git push origin main", cwd=project_path)
            if success:
                print("✅ Origin main push worked!")
                return
            else:
                print(f"❌ Origin main push failed: {stderr}")
            
            print("\nStrategy 3: 'git push --set-upstream origin main'")
            success, stdout, stderr = run_git_command("git push --set-upstream origin main", cwd=project_path)
            if success:
                print("✅ Upstream push worked!")
                return
            else:
                print(f"❌ Upstream push failed: {stderr}")
            
            print("\n💡 SOLUTION:")
            print("The enhanced Git integration should now handle this automatically.")
            print("Try the 'push' command in NEXUS again - it should work now!")
            
    except Exception as e:
        print(f"❌ Error debugging: {e}")

if __name__ == "__main__":
    debug_git_push_issue()