# Enhanced VS Code Integration for NEXUS Project Mode
# This module provides seamless integration with VS Code workflow

import os
import json
import subprocess
from datetime import datetime
import sys
sys.path.append(os.path.dirname(__file__))
from ProjectContext import load_current_project_context, get_current_project_path

class VSCodeProjectManager:
    """Manages active VS Code projects and provides contextual assistance"""
    
    def __init__(self):
        self.current_project = None
        self.project_history = []
        self.vscode_workspaces = []
        
    def detect_vscode_projects(self):
        """Detect currently open VS Code projects"""
        try:
            # Check for VS Code processes and open folders
            result = subprocess.run(
                ['powershell', '-Command', 'Get-Process Code -ErrorAction SilentlyContinue | Select-Object -ExpandProperty MainWindowTitle'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                windows = result.stdout.strip().split('\n')
                projects = []
                for window in windows:
                    if window and ' - Visual Studio Code' in window:
                        project_name = window.replace(' - Visual Studio Code', '').strip()
                        if project_name and project_name != 'Visual Studio Code':
                            projects.append(project_name)
                return projects
        except Exception as e:
            print(f"Could not detect VS Code projects: {e}")
        
        return []
    
    def set_active_project(self, project_name):
        """Set the active project for contextual commands"""
        projects_data = self.load_nexus_projects()
        
        # Find project in NEXUS data
        for project in projects_data.get('active_projects', []):
            if project['name'].lower() == project_name.lower():
                self.current_project = project
                self.project_history.append({
                    'name': project_name,
                    'timestamp': datetime.now().isoformat(),
                    'path': project.get('local_path', '')
                })
                return True, f"✅ Switched to project: {project_name}"
        
        return False, f"❌ Project '{project_name}' not found in NEXUS"
    
    def get_current_project_path(self):
        """Get the file path of currently active project"""
        if self.current_project:
            return self.current_project.get('local_path', os.getcwd())
        return os.getcwd()
    
    def get_contextual_git_commands(self):
        """Get Git commands relevant to current project"""
        # Use persistent context instead of self.current_project
        current_project = load_current_project_context()
        if not current_project:
            return "⚠️ No active project set. Use 'switch to [project_name]' first."
            
        project_name = current_project['name']
        project_path = get_current_project_path()
        
        return f"""🔄 **Git Commands for {project_name}**

**Quick Commands:**
• `git status` - Check current changes
• `git add .` - Stage all changes  
• `git commit` - Commit with message
• `claim commit "your message"` - Quick commit
• `git push` - Push to remote
• `git pull` - Pull latest changes

**Branch Management:**
• `git branch` - List branches
• `git checkout -b feature-name` - Create new branch
• `switch branch main` - Switch to main branch

**Project Path:** `{project_path}`
**Git Integration:** {'✅ Active' if current_project.get('git_initialized') else '❌ Not initialized'}"""
    
    def execute_contextual_git_command(self, command):
        """Execute Git command in current project context"""
        # Use persistent context instead of self.current_project
        current_project = load_current_project_context()
        if not current_project:
            return False, "No active project set. Use 'switch to [project_name]' first."
            
        project_path = get_current_project_path()
        
        # Ensure we're in a git repository
        if not os.path.exists(os.path.join(project_path, '.git')):
            return False, f"Project '{current_project['name']}' is not a Git repository. Use 'git init' first."
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=project_path, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            return success, output.strip()
            
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def load_nexus_projects(self):
        """Load projects from NEXUS data"""
        try:
            with open(r"Data\projects.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"active_projects": []}
    
    def get_project_status(self):
        """Get current project status and recent activity"""
        if not self.current_project:
            vscode_projects = self.detect_vscode_projects()
            
            status = "🔍 **Project Detection**\n\n"
            if vscode_projects:
                status += "📝 **Open in VS Code:**\n"
                for i, proj in enumerate(vscode_projects, 1):
                    status += f"{i}. {proj}\n"
                status += "\n💡 Say 'switch to [project_name]' to set active project"
            else:
                status += "❌ No VS Code projects detected\n"
                status += "💡 Open a project in VS Code or use 'switch to [project_name]'"
            
            return status
        
        project = self.current_project
        project_path = self.get_current_project_path()
        
        status = f"""🎯 **Active Project: {project['name']}**

📁 **Path:** `{project_path}`
📅 **Created:** {project.get('created_date', 'Unknown')}
⏰ **Deadline:** {project.get('deadline', 'Not set')}
📊 **Progress:** {project.get('progress', 0)}%
🔧 **Type:** {project.get('type', 'Unknown')}

🔄 **Git Status:** {'✅ Initialized' if project.get('git_initialized') else '❌ Not initialized'}
🌐 **GitHub:** {project.get('github_repo', 'Not connected')}

💡 **Quick Actions:**
• `git status` - Check changes
• `commit changes` - Quick commit
• `project progress` - Update progress
• `switch to [other_project]` - Change project"""

        return status

# Global instance for the session
vscode_manager = VSCodeProjectManager()

def handle_vscode_integration(query):
    """Handle VS Code integration commands"""
    global vscode_manager
    query_lower = query.lower()
    
    # Project switching
    if "switch to" in query_lower or "set project" in query_lower:
        project_name = query_lower.replace("switch to", "").replace("set project", "").strip()
        success, message = vscode_manager.set_active_project(project_name)
        return message
    
    # Git commands with context
    elif query_lower.startswith(("git ", "commit ", "push", "pull")):
        if query_lower == "git status":
            success, output = vscode_manager.execute_contextual_git_command("git status")
            return f"📋 **Git Status**\n```\n{output}\n```" if success else f"❌ {output}"
        
        elif query_lower.startswith("commit "):
            message = query[7:].strip()  # Remove "commit "
            if message:
                success, output = vscode_manager.execute_contextual_git_command(f'git add . && git commit -m "{message}"')
                return f"✅ **Committed:** {message}\n```\n{output}\n```" if success else f"❌ {output}"
            else:
                return "❌ Please provide a commit message: `commit your message here`"
        
        elif query_lower in ["push", "git push"]:
            success, output = vscode_manager.execute_contextual_git_command("git push")
            return f"🚀 **Pushed to remote**\n```\n{output}\n```" if success else f"❌ {output}"
        
        elif query_lower in ["pull", "git pull"]:
            success, output = vscode_manager.execute_contextual_git_command("git pull")
            return f"⬇️ **Pulled from remote**\n```\n{output}\n```" if success else f"❌ {output}"
        
        elif query_lower in ["git init", "init"]:
            # Special handling for git init - don't check if repo exists, just initialize
            return None  # Let ProjectAgent handle git init
        
        else:
            # Generic git command
            success, output = vscode_manager.execute_contextual_git_command(query)
            return f"```\n{output}\n```" if success else f"❌ {output}"
    
    # Project status and detection
    elif "current project" in query_lower or "project status" in query_lower:
        return vscode_manager.get_project_status()
    
    # Git help
    elif "git help" in query_lower or "git commands" in query_lower:
        return vscode_manager.get_contextual_git_commands()
    
    # Detect VS Code projects
    elif "detect projects" in query_lower or "find projects" in query_lower:
        projects = vscode_manager.detect_vscode_projects()
        if projects:
            result = "📝 **VS Code Projects Detected:**\n\n"
            for i, proj in enumerate(projects, 1):
                result += f"{i}. {proj}\n"
            result += "\n💡 Use 'switch to [project_name]' to set active project"
            return result
        else:
            return "❌ No VS Code projects currently open"
    
    return None  # Let other handlers process the query