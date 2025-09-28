"""
Quick Git Commands for Active Development
Provides instant Git operations while coding in VS Code
"""

import os
from .GitIntegration import handle_git_command, get_project_git_info

def get_current_project():
    """Get current project - moved here to avoid circular import"""
    try:
        import json
        with open(r"Data\projects.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        active_projects = data.get("active_projects", [])
        if active_projects:
            # Default to first project or project with ID 2 if available
            for project in active_projects:
                if project["id"] == 2:
                    return project
            return active_projects[0]
    except:
        pass
    return None

def quick_commit(message="Quick save"):
    """Quick commit with auto-generated or custom message"""
    project = get_current_project()
    if not project:
        return "❌ No active project. Switch to a project first."
    
    command = f"git commit \"{message}\""
    success, result = handle_git_command(command, project)
    return f"{'✅' if success else '❌'} {result}"

def quick_push():
    """Quick push - commits and pushes in one command"""
    project = get_current_project()
    if not project:
        return "❌ No active project. Switch to a project first."
    
    success, result = handle_git_command("git push", project)
    return f"{'✅' if success else '❌'} {result}"

def quick_status():
    """Quick status check"""
    project = get_current_project()
    if not project:
        return "❌ No active project. Switch to a project first."
    
    success, result = handle_git_command("git status", project)
    return result

def quick_sync():
    """Quick sync - pull then push"""
    project = get_current_project()
    if not project:
        return "❌ No active project. Switch to a project first."
    
    # First pull
    success, pull_result = handle_git_command("git pull", project)
    if not success:
        return f"❌ Pull failed: {pull_result}"
    
    # Then push if there are local changes
    git_info = get_project_git_info(project.get("local_path", ""))
    if git_info.get("has_changes", False):
        success, push_result = handle_git_command("git push", project)
        return f"🔄 Sync complete:\n📥 {pull_result}\n📤 {push_result}"
    else:
        return f"🔄 Sync complete:\n📥 {pull_result}\n📤 No local changes to push"

# Quick command mappings for natural language
QUICK_COMMANDS = {
    "save": quick_commit,
    "commit": quick_commit, 
    "push": quick_push,
    "status": quick_status,
    "sync": quick_sync,
    "save and push": quick_push,
    "commit and push": quick_push,
    "check status": quick_status,
    "git status": quick_status,
    "quick save": lambda: quick_commit("Quick save"),
    "backup": lambda: quick_commit("Backup progress"),
}

def handle_quick_git(command):
    """Handle quick git commands with natural language"""
    command_lower = command.lower().strip()
    
    # Direct command mapping
    if command_lower in QUICK_COMMANDS:
        return QUICK_COMMANDS[command_lower]()
    
    # Custom commit message
    if "commit" in command_lower and ("with message" in command_lower or "\"" in command):
        import re
        msg_match = re.search(r'(?:commit|save).*?(?:message|msg)?\s*["\']?(.*?)["\']?$', command, re.IGNORECASE)
        if msg_match:
            message = msg_match.group(1).strip()
            return quick_commit(message)
    
    # Fallback to regular git handling
    project = get_current_project()
    if project:
        success, result = handle_git_command(command, project)
        return f"{'✅' if success else '❌'} {result}"
    else:
        return "❌ No active project. Switch to a project first."