import subprocess
import os
import json
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

def create_github_repo(repo_name, description="", private=True):
    """Create GitHub repository using GitHub CLI"""
    visibility = "--private" if private else "--public"
    desc_flag = f'--description "{description}"' if description else ""
    
    command = f'gh repo create {repo_name} {visibility} {desc_flag} --confirm'
    success, stdout, stderr = run_git_command(command)
    
    if success:
        return True, f"GitHub repository '{repo_name}' created successfully"
    else:
        return False, f"Failed to create GitHub repo: {stderr}"

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
        if not success and "nothing to commit" not in stderr:
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
    
    if not project_path or not os.path.exists(project_path):
        return False, "Project path not found. Please set project directory first."
    
    command_lower = command.lower()
    
    # Initialize repository
    if "init" in command_lower or "initialize" in command_lower:
        return init_git_repo(project_path, project_name)
    
    # Create GitHub repository
    elif "create repo" in command_lower or "create github" in command_lower:
        description = project_data.get("description", "")
        return create_github_repo(project_name, description)
    
    # Push to GitHub
    elif "push" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return False, "Not a git repository. Initialize first with 'git init'"
        
        if not git_info["has_remote"]:
            return False, "No remote repository configured. Create GitHub repo first."
        
        if not git_info["has_changes"]:
            return True, "No changes to push"
        
        commit_msg = f"Project update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        return push_to_github(project_path, git_info["branch"], commit_msg)
    
    # Check status
    elif "status" in command_lower:
        git_info = get_project_git_info(project_path)
        
        if not git_info["is_git_repo"]:
            return True, "❌ Not a git repository"
        
        status_msg = f"""📋 GIT STATUS:
• Repository: ✅ Initialized
• Remote: {'✅ ' + git_info['remote_url'] if git_info['has_remote'] else '❌ Not configured'}
• Branch: {git_info['branch']}
• Changes: {'⚠️ Uncommitted changes' if git_info['has_changes'] else '✅ Clean working directory'}"""
        
        return True, status_msg
    
    else:
        return False, "Unknown git command. Available: init, create repo, push, status"

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