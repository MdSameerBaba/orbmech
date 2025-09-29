import subprocess
import os
import json
import requests
from datetime import datetime

def run_git_command(command, cwd=None):
    """Execute git command and return result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_git_status(project_path):
    """Check if directory has uncommitted changes"""
    if not os.path.exists(os.path.join(project_path, '.git')):
        return False, "Not a git repository"
    
    success, stdout, stderr = run_git_command("git status --porcelain", cwd=project_path)
    if success:
        has_changes = len(stdout.strip()) > 0
        return has_changes, stdout
    return False, stderr

def init_git_repo(project_path, project_name):
    """Initialize git repository"""
    if os.path.exists(os.path.join(project_path, '.git')):
        return True, "Repository already exists"
    
    commands = [
        "git init",
        "git add .",
        f'git commit -m "Initial commit for {project_name}"'
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_git_command(cmd, cwd=project_path)
        if not success:
            return False, f"Failed: {cmd} - {stderr}"
    
    return True, "Git repository initialized successfully"

def generate_alternative_repo_names(base_name):
    """Generate alternative repository names"""
    import re
    # Clean the base name
    clean_name = re.sub(r'\s+', '-', base_name.lower())
    clean_name = re.sub(r'[^a-zA-Z0-9\-_]', '', clean_name)
    
    alternatives = [
        f"{clean_name}-v2",
        f"{clean_name}-new", 
        f"{clean_name}-project",
        f"{clean_name}-{datetime.now().strftime('%Y%m%d')}",
        f"{clean_name}-repo",
        f"my-{clean_name}"
    ]
    return alternatives

def create_github_repo(repo_name, description="", private=True, project_path=None):
    """Create GitHub repository using GitHub CLI and optionally connect local repo"""
    visibility = "--private" if private else "--public"
    desc_flag = f'--description "{description}"' if description else ""
    
    # Updated command without deprecated --confirm flag - quote repo name to handle spaces
    command = f'gh repo create "{repo_name}" {visibility} {desc_flag}'
    success, stdout, stderr = run_git_command(command)
    
    if success:
        message = f"GitHub repository '{repo_name}' created successfully"
        
        # If project_path is provided, automatically connect the local repo
        if project_path and os.path.exists(project_path):
            try:
                # Get GitHub username from gh CLI
                username_success, username, _ = run_git_command("gh api user --jq .login")
                if username_success:
                    repo_url = f"https://github.com/{username}/{repo_name}.git"
                    
                    # Check if remote already exists
                    check_success, remotes, _ = run_git_command("git remote -v", cwd=project_path)
                    if check_success and "origin" in remotes:
                        # Remove existing remote
                        run_git_command("git remote remove origin", cwd=project_path)
                    
                    # Add new remote
                    remote_success, _, remote_error = run_git_command(f"git remote add origin {repo_url}", cwd=project_path)
                    if remote_success:
                        message += f" and connected to local repository"
                    else:
                        message += f" (Warning: Could not connect local repo: {remote_error})"
            except Exception as e:
                message += f" (Warning: Could not auto-connect local repo: {e})"
        
        return True, message
    else:
        # Check for specific error types
        if "token has not been granted" in stderr.lower() or "scopes" in stderr.lower():
            return False, f"❌ GitHub token missing required permissions.\n\nYour token needs 'repo' or 'public_repo' scope.\n\n🔧 To fix:\n1. Go to https://github.com/settings/tokens\n2. Edit your token or create new one\n3. Check 'repo' scope (full repository access)\n4. Update GITHUB_TOKEN in .env file\n5. Restart the application\n\nCurrent error: {stderr}"
        elif "name already exists" in stderr.lower() or "already exists" in stderr.lower():
            # Repository name already exists - suggest alternatives
            alternatives = generate_alternative_repo_names(repo_name)
            alt_list = "\n".join([f"   • {alt}" for alt in alternatives[:4]])
            return False, f"❌ Repository name '{repo_name}' already exists on GitHub.\n\n💡 **Solutions:**\n\n1. **Choose new name:** Try one of these alternatives:\n{alt_list}\n\n2. **Connect to existing:** If you want to use the existing repo:\n   • git remote add origin https://github.com/[username]/{repo_name}.git\n   • Then use 'push' command\n\n3. **Delete existing:** Go to GitHub.com and delete the existing repo first\n\n🎯 **Quick fix:** Rename your project or try a suggested alternative name."
        elif "--confirm has been deprecated" in stderr:
            return False, f"❌ GitHub CLI version issue. Command updated but still failing.\n\nError: {stderr}"
        return False, f"Failed to create GitHub repo: {stderr}"

def connect_to_existing_repo(project_path, repo_name, username):
    """Connect local repository to existing GitHub repo"""
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    
    # Check if remote already exists
    check_remote_cmd = "git remote -v"
    success, stdout, stderr = run_git_command(check_remote_cmd, cwd=project_path)
    
    if success and "origin" in stdout:
        return False, "❌ Remote origin already exists. Use 'git remote remove origin' first if you want to change it."
    
    # Add the remote
    command = f"git remote add origin {repo_url}"
    success, stdout, stderr = run_git_command(command, cwd=project_path)
    
    if success:
        return True, f"✅ Connected to existing repository: {repo_url}"
    else:
        return False, f"❌ Failed to connect to repository: {stderr}"

def add_remote_origin(project_path, repo_url):
    """Add remote origin to local repository"""
    command = f"git remote add origin {repo_url}"
    success, stdout, stderr = run_git_command(command, cwd=project_path)
    
    if success:
        return True, "Remote origin added successfully"
    else:
        return False, f"Failed to add remote: {stderr}"

def push_to_github(project_path, branch="main", commit_message=None):
    """Push changes to GitHub"""
    if commit_message is None:
        commit_message = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    commands = [
        "git add .",
        f'git commit -m "{commit_message}"',
        f"git push -u origin {branch}"
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_git_command(cmd, cwd=project_path)
        if not success and "nothing to commit" not in stderr and "up-to-date" not in stderr:
            return False, f"Failed: {cmd} - {stderr}"
    
    return True, "Successfully pushed to GitHub"

def get_project_git_info(project_path):
    """Get git information for a project"""
    if not os.path.exists(os.path.join(project_path, '.git')):
        return {
            "is_git_repo": False,
            "has_remote": False,
            "has_changes": False,
            "branch": None,
            "remote_url": None
        }
    
    # Check current branch
    success, branch, _ = run_git_command("git branch --show-current", cwd=project_path)
    current_branch = branch if success else "main"
    
    # Check remote URL
    success, remote_url, _ = run_git_command("git remote get-url origin", cwd=project_path)
    has_remote = success and remote_url
    
    # Check for uncommitted changes
    has_changes, _ = check_git_status(project_path)
    
    return {
        "is_git_repo": True,
        "has_remote": has_remote,
        "has_changes": has_changes,
        "branch": current_branch,
        "remote_url": remote_url if has_remote else None
    }

def handle_git_command(command, project_data):
    """Handle various git commands"""
    project_name = project_data.get("name", "")
    project_path = project_data.get("local_path", "")
    
    if not project_path:
        return False, "Project path not found. Please set project directory first."
    
    # Create directory if it doesn't exist
    if not os.path.exists(project_path):
        try:
            os.makedirs(project_path, exist_ok=True)
        except Exception as e:
            return False, f"Could not create directory {project_path}: {e}"
    
    command_lower = command.lower()
    
    # Initialize repository
    if "init" in command_lower or "initialize" in command_lower:
        return init_git_repo(project_path, project_name)
    
    # Create GitHub repository
    elif "create repo" in command_lower or "create github" in command_lower:
        description = project_data.get("description", "")
        try:
            return create_github_repo(project_name, description, project_path=project_path)
        except Exception as e:
            return False, f"Failed to create GitHub repo: {e}"
    
    # Commit changes
    elif "commit" in command_lower:
        # Extract commit message if provided
        import re
        msg_match = re.search(r'commit[\s"\']+(.*?)(?:["\']|$)', command, re.IGNORECASE)
        commit_msg = msg_match.group(1).strip() if msg_match else f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        commands = [
            "git add .",
            f'git commit -m "{commit_msg}"'
        ]
        
        for cmd in commands:
            success, stdout, stderr = run_git_command(cmd, cwd=project_path)
            if not success and "nothing to commit" not in stderr:
                return False, f"Commit failed: {stderr}"
        
        return True, f"✅ Changes committed: '{commit_msg}'"
    
    # Add remote repository (simplified version)
    elif "remote add" in command_lower or "add remote" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return False, "Not a git repository. Initialize first with 'git init'"
        
        # Check if remote already exists
        if git_info["has_remote"]:
            return False, f"Remote origin already configured: {git_info['remote_url']}"
        
        # Auto-construct GitHub URL using project name
        # Try to get GitHub username from gh CLI or git config
        success, username, stderr = run_git_command("gh api user --jq .login", cwd=project_path)
        
        if not success:
            # Fallback: try git config
            success, username, stderr = run_git_command("git config user.name", cwd=project_path)
            if not success:
                return False, "❌ Could not determine GitHub username. Please run 'gh auth login' first or set 'git config user.name'"
        
        username = username.strip()
        github_url = f"https://github.com/{username}/{project_name}.git"
        
        # Add remote origin
        success, stdout, stderr = run_git_command(f"git remote add origin {github_url}", cwd=project_path)
        
        if success:
            return True, f"✅ Added remote origin: {github_url}"
        else:
            return False, f"Failed to add remote: {stderr}"
    
    # Push to GitHub
    elif "push" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return False, "Not a git repository. Initialize first with 'git init'"
        
        if not git_info["has_remote"]:
            return False, "No remote repository configured. Create GitHub repo first."
        
        # Auto-commit if there are changes
        if git_info["has_changes"]:
            commit_msg = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            success, stdout, stderr = run_git_command(f'git add . && git commit -m "{commit_msg}"', cwd=project_path)
            if not success and "nothing to commit" not in stderr:
                return False, f"Auto-commit failed: {stderr}"
        
        # Push to remote - Enhanced with multiple fallback strategies
        branch = git_info['branch'] if git_info['branch'] else 'main'
        
        print(f"🚀 Attempting to push branch '{branch}' to GitHub...")
        
        # Strategy 1: Try simple push first
        success, stdout, stderr = run_git_command("git push", cwd=project_path)
        
        if success:
            return True, f"✅ Successfully pushed to GitHub ({branch} branch)"
        
        # Strategy 2: If that fails, try with origin and branch
        if not success:
            print(f"🔧 Simple push failed, trying with origin {branch}...")
            success, stdout, stderr = run_git_command(f"git push origin {branch}", cwd=project_path)
            
            if success:
                return True, f"✅ Successfully pushed to GitHub ({branch} branch)"
        
        # Strategy 3: If still fails, check for upstream issues and set upstream
        if not success and ("no upstream" in stderr.lower() or "no tracking information" in stderr.lower() or "fatal" in stderr.lower() or "destination" in stderr.lower()):
            print(f"🔧 Setting upstream branch for {branch}...")
            
            # Ensure we're on the right branch first
            run_git_command(f"git checkout -b {branch}", cwd=project_path)  # Create branch if needed
            run_git_command(f"git branch -M {branch}", cwd=project_path)    # Rename to main/master
            
            # Set upstream and push
            success, stdout, stderr = run_git_command(f"git push --set-upstream origin {branch}", cwd=project_path)
            
            if success:
                return True, f"✅ Successfully pushed to GitHub with upstream setup ({branch} branch)"
            else:
                # Strategy 4: Last resort - force push with upstream
                print(f"🔧 Trying force push with upstream...")
                success, stdout, stderr = run_git_command(f"git push -u origin {branch} --force", cwd=project_path)
                
                if success:
                    return True, f"✅ Successfully force pushed to GitHub with upstream setup ({branch} branch)"
                else:
                    return False, f"❌ All push strategies failed. Last error: {stderr}\n\n💡 Suggestions:\n1. Check if GitHub repo exists\n2. Verify remote origin is set: git remote -v\n3. Check GitHub authentication: gh auth status"
        else:
            return False, f"Push failed: {stderr}"
    
    # Pull from GitHub
    elif "pull" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return False, "Not a git repository. Initialize first with 'git init'"
        
        if not git_info["has_remote"]:
            return False, "No remote repository configured."
        
        success, stdout, stderr = run_git_command(f"git pull origin {git_info['branch']}", cwd=project_path)
        if success:
            return True, f"✅ Successfully pulled from GitHub\n{stdout}"
        else:
            return False, f"Pull failed: {stderr}"
    
    # Check status
    elif "status" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return True, "❌ Not a git repository"
        
        # Get detailed status
        success, status_output, _ = run_git_command("git status --short", cwd=project_path)
        
        status_msg = f"""📋 GIT STATUS for '{project_name}':
• Repository: ✅ Initialized
• Remote: {'✅ ' + git_info['remote_url'] if git_info['has_remote'] else '❌ Not configured'}
• Branch: {git_info['branch']}
• Changes: {'⚠️ Uncommitted changes' if git_info['has_changes'] else '✅ Clean working directory'}"""
        
        if git_info["has_changes"] and status_output:
            status_msg += f"\n\n📝 Modified files:\n{status_output}"
        
        return True, status_msg
    
    # Add specific files
    elif "add" in command_lower:
        # Extract file pattern if provided
        import re
        file_match = re.search(r'add\s+(.+)', command, re.IGNORECASE)
        files = file_match.group(1).strip() if file_match else "."
        
        success, stdout, stderr = run_git_command(f"git add {files}", cwd=project_path)
        if success:
            return True, f"✅ Added files to staging: {files}"
        else:
            return False, f"Add failed: {stderr}"
    
    else:
        return False, """❌ Unknown git command. Available commands:
• 'git init' - Initialize repository
• 'git status' - Check repository status
• 'git add .' - Stage all changes
• 'git commit "message"' - Commit changes
• 'git remote add' - Connect to GitHub repository (auto-detects URL)
• 'git push' - Push to GitHub (auto-commits if needed)
• 'git pull' - Pull from GitHub
• 'create github repo' - Create GitHub repository"""

def check_exit_warning(project_data):
    """Check if project has uncommitted changes when exiting project mode"""
    project_path = project_data.get("local_path", "")
    
    if not project_path or not os.path.exists(project_path):
        return False, ""
    
    git_info = get_project_git_info(project_path)
    
    if git_info["is_git_repo"] and git_info["has_changes"]:
        return True, f"""⚠️ UNCOMMITTED CHANGES DETECTED

Project: {project_data.get('name', 'Unknown')}
Path: {project_path}

You have uncommitted changes that haven't been pushed to Git.
Your progress may be lost if not saved.

Would you like to:
• Push changes to GitHub: "push to git"
• Continue without saving: "ignore changes"
• Stay in project mode: "cancel exit"
"""
    
    return False, ""