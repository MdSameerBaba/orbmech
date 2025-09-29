"""
Fix NEXUS project context - Switch to Enhanced Vue Ecommerce
"""
import json
import os
from datetime import datetime

def update_nexus_context():
    """Update NEXUS to use Enhanced Vue Ecommerce project"""
    
    context_file = "Data/current_context.json"
    projects_file = "Data/projects.json"
    
    try:
        # Load projects to get Enhanced Vue Ecommerce details
        with open(projects_file, 'r', encoding='utf-8') as f:
            projects_data = json.load(f)
        
        # Find Enhanced Vue Ecommerce project (ID 28)
        enhanced_project = None
        for project in projects_data["active_projects"]:
            if project["name"] == "Enhanced Vue Ecommerce":
                enhanced_project = project
                break
        
        if not enhanced_project:
            print("❌ Enhanced Vue Ecommerce project not found!")
            return False
        
        # Create new context pointing to Enhanced Vue Ecommerce
        new_context = {
            "current_project": enhanced_project,
            "last_updated": datetime.now().isoformat(),
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        # Save new context
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(new_context, f, indent=2, ensure_ascii=False)
        
        print("✅ NEXUS context updated successfully!")
        print(f"📛 Current Project: {enhanced_project['name']}")
        print(f"🆔 Project ID: {enhanced_project['id']}")
        print(f"📁 Project Path: {enhanced_project['local_path']}")
        print(f"🏗️  Tech Stack: Vue + Node.js + MongoDB")
        print(f"📄 Files: 43 production-ready files")
        print()
        print("🎯 Next Steps:")
        print("1. Restart NEXUS: python Main.py")
        print("2. Try: project git init")
        print("3. Try: project create github repo")
        print("4. Try: project push to git")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating context: {e}")
        return False

if __name__ == "__main__":
    update_nexus_context()