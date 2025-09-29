"""
Fix upstream branch setup for Enhanced Vue Ecommerce
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

def setup_upstream_branch():
    """Setup upstream branch for the Enhanced Vue Ecommerce project"""
    
    project_path = r"C:\Users\mdsam\OneDrive\Desktop\orbmech\Backend\EcommerceApp"
    
    print("🔧 Setting up upstream branch for Enhanced Vue Ecommerce...")
    print(f"📁 Project Path: {project_path}")
    print()
    
    if not os.path.exists(project_path):
        print(f"❌ Project directory not found: {project_path}")
        return False
    
    # Step 1: Check current status
    print("📊 Checking current Git status...")
    success, stdout, stderr = run_git_command("git status", cwd=project_path)
    if not success:
        print(f"❌ Not a git repository: {stderr}")
        return False
    
    # Step 2: Check if remote exists
    success, stdout, stderr = run_git_command("git remote -v", cwd=project_path)
    if not success or "origin" not in stdout:
        print("❌ No remote origin found. Setting up remote first...")
        
        # Add remote origin
        repo_url = "https://github.com/MdSameerBaba/Enhanced-Vue-Ecommerce.git"
        success, stdout, stderr = run_git_command(f"git remote add origin {repo_url}", cwd=project_path)
        if not success:
            print(f"❌ Failed to add remote: {stderr}")
            return False
        print(f"✅ Added remote origin: {repo_url}")
    else:
        print("✅ Remote origin already configured")
    
    # Step 3: Ensure we're on main branch
    print("🌿 Ensuring we're on main branch...")
    success, stdout, stderr = run_git_command("git branch -M main", cwd=project_path)
    if not success:
        print(f"⚠️ Warning: {stderr}")
    else:
        print("✅ On main branch")
    
    # Step 4: Add and commit any changes
    print("💾 Adding and committing any changes...")
    success, stdout, stderr = run_git_command("git add .", cwd=project_path)
    success, stdout, stderr = run_git_command('git commit -m "Setup: Enhanced Vue Ecommerce with full-stack architecture"', cwd=project_path)
    if not success and "nothing to commit" not in stderr:
        print(f"⚠️ Commit warning: {stderr}")
    else:
        print("✅ Changes committed")
    
    # Step 5: Set upstream and push
    print("🚀 Setting upstream branch and pushing...")
    success, stdout, stderr = run_git_command("git push --set-upstream origin main", cwd=project_path)
    if not success:
        print(f"❌ Failed to set upstream: {stderr}")
        print("\n💡 Possible solutions:")
        print("1. Make sure GitHub repo 'Enhanced-Vue-Ecommerce' exists")
        print("2. Check your GitHub authentication (gh auth login)")
        print("3. Verify repository permissions")
        return False
    
    print("🎉 SUCCESS! Upstream branch configured!")
    print("✅ Your Enhanced Vue Ecommerce project is now connected to GitHub")
    print()
    print("🎯 Now you can use NEXUS commands:")
    print("• 'push' - Push changes to GitHub")
    print("• 'pull' - Pull changes from GitHub") 
    print("• 'git status' - Check repository status")
    
    return True

if __name__ == "__main__":
    setup_upstream_branch()