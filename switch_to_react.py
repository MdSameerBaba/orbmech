"""
Switch NEXUS context to React Social Media project
"""
import json
import os
from datetime import datetime

def switch_to_react_social_media():
    """Switch NEXUS context to React Social Media project"""
    
    context_file = "Data/current_context.json"
    projects_file = "Data/projects.json"
    
    try:
        # Load projects to find React Social Media (ID: 29)
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects_data = json.load(f)
        
        # Find React Social Media project
        react_project = None
        for project in projects_data["active_projects"]:
            if project["name"] == "React Social Media" and project["id"] == 29:
                react_project = project
                break
        
        if not react_project:
            print("❌ React Social Media project (ID: 29) not found!")
            print("🔍 Looking for any React Social Media project...")
            
            # Try to find any React Social Media project
            for project in projects_data["active_projects"]:
                if "React Social Media" in project["name"]:
                    react_project = project
                    print(f"✅ Found: {project['name']} (ID: {project['id']})")
                    break
        
        if not react_project:
            print("❌ No React Social Media project found in database!")
            return False
        
        # Update the project with correct path
        react_project["local_path"] = "C:\\Users\\mdsam\\Desktop\\ReactSocialMedia"
        react_project["git_initialized"] = False  # Reset git status
        react_project["github_repo"] = ""  # Reset GitHub repo
        
        # Create new context pointing to React Social Media
        new_context = {
            "current_project": react_project,
            "last_updated": datetime.now().isoformat(),
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        # Save new context
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(new_context, f, indent=2, ensure_ascii=False)
        
        print("✅ NEXUS context switched successfully!")
        print(f"📛 Current Project: {react_project['name']}")
        print(f"🆔 Project ID: {react_project['id']}")
        print(f"📁 Project Path: {react_project['local_path']}")
        print(f"🏗️  Tech Stack: React with Real-time Chat")
        print(f"📄 Generated Files: 12 files")
        print()
        print("🎯 Next Steps:")
        print("1. Restart NEXUS: python Main.py")
        print("2. NEXUS should now show 'React Social Media' as current project")
        print("3. Try: git init")
        print("4. Try: create github repo")
        print("5. Try: push")
        
        return True
        
    except Exception as e:
        print(f"❌ Error switching context: {e}")
        return False

if __name__ == "__main__":
    switch_to_react_social_media()