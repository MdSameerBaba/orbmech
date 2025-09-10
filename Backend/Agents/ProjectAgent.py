import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import dotenv_values
from groq import Groq
import threading
import time
from .GitIntegration import handle_git_command, check_exit_warning, get_project_git_info
from .GitHubSetup import setup_github_credentials, verify_github_setup, get_github_credentials

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in ProjectAgent: {e}")
    client = None

PROJECTS_FILE = r"Data\projects.json"

# --- PROJECT MANAGEMENT FUNCTIONS ---
def load_projects():
    """Load projects data"""
    try:
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"active_projects": [], "completed_projects": [], "project_templates": {}}

def save_projects(data):
    """Save projects data"""
    try:
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"❌ Error saving projects: {e}")
        return False

def create_project(name, description, deadline, project_type="custom"):
    """Create a new project"""
    data = load_projects()
    
    project = {
        "id": len(data["active_projects"]) + len(data["completed_projects"]) + 1,
        "name": name,
        "description": description,
        "type": project_type,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "deadline": deadline,
        "status": "active",
        "progress": 0,
        "tasks": [],
        "time_spent": 0,
        "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "local_path": "",
        "github_repo": "",
        "git_initialized": False
    }
    
    # Add template tasks if available
    templates = data.get("project_templates", {})
    if project_type in templates:
        template = templates[project_type]
        for task in template.get("default_tasks", []):
            project["tasks"].append({
                "name": task["name"],
                "phase": task["phase"],
                "estimated_hours": task["estimated_hours"],
                "actual_hours": 0,
                "status": "pending",
                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    data["active_projects"].append(project)
    save_projects(data)
    
    return f"✅ Project '{name}' created successfully! ID: {project['id']}"

def get_active_projects():
    """Get all active projects"""
    data = load_projects()
    return data.get("active_projects", [])

def update_project_progress(project_id, progress):
    """Update project progress"""
    data = load_projects()
    
    for project in data["active_projects"]:
        if project["id"] == project_id:
            project["progress"] = min(100, max(0, progress))
            project["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if progress >= 100:
                project["status"] = "completed"
                data["completed_projects"].append(project)
                data["active_projects"].remove(project)
            
            save_projects(data)
            return f"✅ Project progress updated to {progress}%"
    
    return "❌ Project not found"

def log_work_session(project_id, hours, description=""):
    """Log work session for a project"""
    data = load_projects()
    
    for project in data["active_projects"]:
        if project["id"] == project_id:
            project["time_spent"] += hours
            project["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add work log entry
            if "work_logs" not in project:
                project["work_logs"] = []
            
            project["work_logs"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hours": hours,
                "description": description
            })
            
            save_projects(data)
            return f"✅ Logged {hours} hours of work on '{project['name']}'"
    
    return "❌ Project not found"

def check_deadlines():
    """Check for upcoming deadlines"""
    data = load_projects()
    alerts = []
    
    for project in data["active_projects"]:
        deadline = datetime.strptime(project["deadline"], "%Y-%m-%d")
        days_left = (deadline - datetime.now()).days
        
        if days_left <= 7:
            urgency = "🔴 URGENT" if days_left <= 1 else "🟡 WARNING" if days_left <= 3 else "🟠 REMINDER"
            alerts.append(f"{urgency}: '{project['name']}' due in {days_left} days ({project['progress']}% complete)")
    
    return alerts

def generate_project_dashboard():
    """Generate project progress dashboard"""
    data = load_projects()
    active_projects = data.get("active_projects", [])
    
    if not active_projects:
        return "No active projects to display"
    
    # Create dashboard chart
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"{Username}'s Project Dashboard", fontsize=16, fontweight='bold')
    
    # 1. Project Progress Bar Chart
    ax1 = axes[0, 0]
    project_names = [p["name"][:15] + "..." if len(p["name"]) > 15 else p["name"] for p in active_projects]
    progress_values = [p["progress"] for p in active_projects]
    
    bars = ax1.barh(project_names, progress_values, color=['#FF6B6B' if p < 30 else '#FFD93D' if p < 70 else '#6BCF7F' for p in progress_values])
    ax1.set_title('Project Progress (%)', fontweight='bold')
    ax1.set_xlim(0, 100)
    
    # Add progress labels
    for bar, value in zip(bars, progress_values):
        ax1.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{value}%', 
                ha='left', va='center', fontweight='bold')
    
    # 2. Time Spent vs Estimated
    ax2 = axes[0, 1]
    time_spent = [p["time_spent"] for p in active_projects]
    estimated_time = [sum(task.get("estimated_hours", 0) for task in p.get("tasks", [])) for p in active_projects]
    
    x = range(len(project_names))
    ax2.bar([i - 0.2 for i in x], time_spent, 0.4, label='Time Spent', color='#4ECDC4')
    ax2.bar([i + 0.2 for i in x], estimated_time, 0.4, label='Estimated', color='#45B7D1')
    ax2.set_title('Time Tracking (Hours)', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([name[:10] for name in project_names], rotation=45)
    ax2.legend()
    
    # 3. Deadline Timeline
    ax3 = axes[1, 0]
    deadlines = []
    for project in active_projects:
        deadline = datetime.strptime(project["deadline"], "%Y-%m-%d")
        days_left = (deadline - datetime.now()).days
        deadlines.append(days_left)
    
    colors = ['red' if d <= 3 else 'orange' if d <= 7 else 'green' for d in deadlines]
    ax3.scatter(deadlines, project_names, c=colors, s=100, alpha=0.7)
    ax3.set_title('Deadline Timeline (Days Left)', fontweight='bold')
    ax3.set_xlabel('Days Until Deadline')
    ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax3.axvline(x=7, color='orange', linestyle='--', alpha=0.5)
    
    # 4. Project Status Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary_text = f"📊 PROJECT SUMMARY\n\n"
    summary_text += f"Active Projects: {len(active_projects)}\n"
    summary_text += f"Completed: {len(data.get('completed_projects', []))}\n\n"
    
    # Upcoming deadlines
    alerts = check_deadlines()
    if alerts:
        summary_text += "⚠️ ALERTS:\n"
        for alert in alerts[:3]:  # Show top 3 alerts
            summary_text += f"• {alert}\n"
    else:
        summary_text += "✅ No urgent deadlines"
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Save chart
    chart_path = r"Data\project_dashboard.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_path

def set_project_path(project_id, local_path):
    """Set local path for a project"""
    data = load_projects()
    
    for project in data["active_projects"]:
        if project["id"] == project_id:
            project["local_path"] = local_path
            save_projects(data)
            return f"✅ Project path set to: {local_path}"
    
    return "❌ Project not found"

def get_project_exit_warning():
    """Check all active projects for uncommitted changes"""
    data = load_projects()
    warnings = []
    
    for project in data.get("active_projects", []):
        if project.get("local_path"):
            has_warning, warning_msg = check_exit_warning(project)
            if has_warning:
                warnings.append(warning_msg)
    
    return warnings

def ProjectAgent(query: str):
    """Main Project Agent function"""
    if not client:
        return "Project management is not available due to AI model configuration issues."
    
    query_lower = query.lower()
    
    # Handle project creation
    if "create project" in query_lower or "new project" in query_lower:
        # Try to parse full project creation command
        import re
        
        # Pattern to match: create project NAME with description DESC deadline DATE type TYPE
        pattern = r"create project\s+([\w]+)(?:\s+with description\s+['\"]([^'\"]+)['\"])?(?:\s+deadline\s+(\d{4}-\d{2}-\d{2}))?(?:\s+type\s+(\w+))?"
        match = re.search(pattern, query, re.IGNORECASE)
        
        if match:
            name = match.group(1).strip()
            description = match.group(2) or f"Project: {name}"
            deadline = match.group(3) or "2024-12-31"
            project_type = match.group(4) or "custom"
            
            # Create the project
            result = create_project(name, description, deadline, project_type)
            return result
        else:
            # Show help if parsing fails
            return """🚀 CREATE NEW PROJECT

To create a project, provide:
• Project name
• Description  
• Deadline (YYYY-MM-DD)
• Type (optional): software_development, research_project, web_development

Example: "Create project 'Mobile App' with description 'iOS shopping app' deadline 2024-02-15 type software_development"

Or just say: "Create project Mobile App" and I'll guide you through the setup!"""
    
    # Handle dashboard/progress
    elif "dashboard" in query_lower or "progress" in query_lower or "status" in query_lower:
        try:
            chart_path = generate_project_dashboard()
            active_projects = get_active_projects()
            
            if not active_projects:
                return "📋 No active projects found. Create your first project with 'create project [name]'!"
            
            summary = f"📊 PROJECT DASHBOARD for {Username}\n\n"
            
            for project in active_projects:
                deadline = datetime.strptime(project["deadline"], "%Y-%m-%d")
                days_left = (deadline - datetime.now()).days
                
                summary += f"🔹 {project['name']}\n"
                summary += f"   Progress: {project['progress']}% | Time: {project['time_spent']}h\n"
                summary += f"   Deadline: {days_left} days left\n\n"
            
            # Check for alerts
            alerts = check_deadlines()
            if alerts:
                summary += "⚠️ DEADLINE ALERTS:\n"
                for alert in alerts:
                    summary += f"• {alert}\n"
            
            summary += f"\n📈 Dashboard saved to: {chart_path}"
            return summary
            
        except Exception as e:
            return f"Error generating dashboard: {e}"
    
    # Handle GitHub setup
    elif "setup github" in query_lower or "github setup" in query_lower:
        print("🔧 Starting GitHub setup...")
        if setup_github_credentials():
            is_valid, message = verify_github_setup()
            return f"✅ GitHub setup completed!\n\n{message}\n\nYou can now use:\n• 'git init' - Initialize repository\n• 'create github repo' - Create GitHub repository\n• 'push to git' - Push changes"
        else:
            return "❌ GitHub setup failed. Please try again."
    
    # Handle Git commands
    elif any(keyword in query_lower for keyword in ["git", "github", "push", "repo", "commit"]):
        # Check GitHub setup first
        credentials = get_github_credentials()
        if not credentials["username"] or not credentials["token"]:
            return "❌ GitHub not configured. Run 'setup github' first."
        
        active_projects = get_active_projects()
        if not active_projects:
            return "❌ No active projects found. Create a project first."
        
        # Get current project (assume first active project for now)
        current_project = active_projects[0]
        
        # Reload project data to get updated path
        data = load_projects()
        for project in data["active_projects"]:
            if project["id"] == current_project["id"]:
                current_project = project
                break
        
        if "set path" in query_lower or "set project path" in query_lower:
            # Parse path from command
            import re
            path_pattern = r"(?:set project path to|set path to|link project to)\s+(.+)"
            match = re.search(path_pattern, query, re.IGNORECASE)
            
            if match:
                project_path = match.group(1).strip()
                # Set path for the first active project
                result = set_project_path(current_project["id"], project_path)
                return result
            else:
                return """📁 SET PROJECT PATH

To link your project to a local directory:
• "set project path to C:\\Users\\username\\MyProject"
• "link project to /home/user/myproject"

This enables Git integration and automatic push warnings."""
        
        try:
            success, message = handle_git_command(query, current_project)
            return f"{'✅' if success else '❌'} {message}"
        except Exception as e:
            return f"❌ Git operation failed: {e}"
    
    # Handle work logging
    elif "log work" in query_lower or "worked" in query_lower:
        return """⏰ LOG WORK SESSION

Examples:
• "Log 3 hours work on project 1"
• "Worked 2 hours on Mobile App"
• "Log work: 4 hours debugging"

I'll track your time and update project progress!"""
    
    # Handle show projects
    elif "show" in query_lower and "project" in query_lower:
        active_projects = get_active_projects()
        
        if not active_projects:
            return "📋 No active projects found. Create your first project with 'create project [name]'!"
        
        result = "📊 ACTIVE PROJECTS:\n\n"
        for project in active_projects:
            deadline = datetime.strptime(project["deadline"], "%Y-%m-%d")
            days_left = (deadline - datetime.now()).days
            
            result += f"🔹 **{project['name']}** (ID: {project['id']})\n"
            result += f"   📝 {project['description']}\n"
            result += f"   📅 Deadline: {project['deadline']} ({days_left} days left)\n"
            result += f"   📈 Progress: {project['progress']}%\n"
            result += f"   ⏱️ Time spent: {project['time_spent']} hours\n"
            result += f"   🏷️ Type: {project['type']}\n\n"
        
        return result
    
    else:
        # General project advice using AI
        active_projects = get_active_projects()
        context = f"Active Projects: {len(active_projects)} projects in progress"
        
        system_prompt = f"You are Nexus, {Username}'s project management assistant. Provide project management advice and motivation."
        
        messages_to_send = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages_to_send,
                max_tokens=1024,
                temperature=0.7,
                stream=False
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error in ProjectAgent: {e}")
            return "I'm having trouble with project management right now."

# --- BACKGROUND REMINDER SYSTEM ---
def start_project_reminders():
    """Start background thread for project reminders"""
    def reminder_loop():
        while True:
            try:
                alerts = check_deadlines()
                if alerts:
                    print("🔔 PROJECT REMINDERS:")
                    for alert in alerts:
                        print(f"   {alert}")
                
                # Sleep for 1 hour before next check
                time.sleep(3600)
            except Exception as e:
                print(f"❌ Error in reminder system: {e}")
                time.sleep(3600)
    
    reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
    reminder_thread.start()
    print("🔔 Project reminder system started")

if __name__ == "__main__":
    print("ProjectAgent test. Type 'exit' to end.")
    while True:
        user_input = input(f"{Username}: ")
        if user_input.lower() == 'exit':
            break
        response = ProjectAgent(user_input)
        print(f"Nexus: {response}")