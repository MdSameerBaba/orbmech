"""
Quick fix to connect the Enhanced Vue Ecommerce project to its GitHub repository
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

def connect_enhanced_vue_to_github():
    """Connect the Enhanced Vue Ecommerce project to GitHub"""
    
    # Project details
    project_path = r"C:\Users\mdsam\OneDrive\Desktop\orbmech\Backend\EcommerceApp"
    repo_name = "Enhanced-Vue-Ecommerce"  # GitHub-friendly name (no spaces)
    username = "MdSameerBaba"  # Your GitHub username
    
    print(f"🔗 Connecting Enhanced Vue Ecommerce to GitHub...")
    print(f"📁 Project Path: {project_path}")
    print(f"🐙 GitHub Repo: https://github.com/{username}/{repo_name}")
    print()
    
    # Check if directory exists
    if not os.path.exists(project_path):
        print(f"❌ Project directory not found: {project_path}")
        return False
    
    # Change to project directory
    os.chdir(project_path)
    
    # Step 1: Check if git is initialized
    success, stdout, stderr = run_git_command("git status", cwd=project_path)
    if not success:
        print("🚀 Initializing Git repository...")
        success, stdout, stderr = run_git_command("git init", cwd=project_path)
        if not success:
            print(f"❌ Failed to initialize git: {stderr}")
            return False
        print("✅ Git repository initialized")
    
    # Step 2: Add all files
    print("📄 Adding files to git...")
    success, stdout, stderr = run_git_command("git add .", cwd=project_path)
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return False
    print("✅ Files added to staging")
    
    # Step 3: Initial commit
    print("💾 Creating initial commit...")
    success, stdout, stderr = run_git_command('git commit -m "Initial commit: Enhanced Vue Ecommerce App with full-stack architecture"', cwd=project_path)
    if not success and "nothing to commit" not in stderr:
        print(f"❌ Failed to commit: {stderr}")
        return False
    print("✅ Initial commit created")
    
    # Step 4: Check if remote exists
    success, stdout, stderr = run_git_command("git remote -v", cwd=project_path)
    if success and "origin" in stdout:
        print("⚠️ Remote origin already exists, removing it first...")
        run_git_command("git remote remove origin", cwd=project_path)
    
    # Step 5: Add GitHub remote
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"🔗 Adding GitHub remote: {repo_url}")
    success, stdout, stderr = run_git_command(f"git remote add origin {repo_url}", cwd=project_path)
    if not success:
        print(f"❌ Failed to add remote: {stderr}")
        return False
    print("✅ GitHub remote added")
    
    # Step 6: Set upstream and push
    print("🚀 Pushing to GitHub...")
    success, stdout, stderr = run_git_command("git branch -M main", cwd=project_path)  # Ensure main branch
    success, stdout, stderr = run_git_command("git push -u origin main", cwd=project_path)
    if not success:
        print(f"❌ Failed to push: {stderr}")
        print(f"💡 Try: Create the GitHub repo first with name: {repo_name}")
        return False
    
    print("🎉 SUCCESS! Enhanced Vue Ecommerce connected to GitHub!")
    print(f"🌐 Repository URL: https://github.com/{username}/{repo_name}")
    print()
    print("🎯 Now you can use NEXUS commands:")
    print("• 'git status' - Check repository status")
    print("• 'push' - Push changes to GitHub")
    print("• 'pull' - Pull changes from GitHub")
    
    return True

if __name__ == "__main__":
    connect_enhanced_vue_to_github()