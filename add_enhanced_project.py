"""
Quick fix to add the enhanced EcommerceApp to NEXUS database
"""
import json
import os
from datetime import datetime

def add_enhanced_project_to_nexus():
    """Add the enhanced EcommerceApp project to NEXUS database"""
    
    # Path to projects.json
    projects_file = "Data/projects.json"
    
    try:
        # Load existing projects
        with open(projects_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create new enhanced project entry
        enhanced_project = {
            "id": 28,  # New ID
            "name": "Enhanced Vue Ecommerce",
            "description": "Full-stack Vue ecommerce store with payment processing - Enhanced Architecture (43 files)",
            "type": "frontend_development",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": "2025-12-31",
            "status": "active",
            "progress": 100,
            "tasks": [
                {
                    "name": "Enhanced Architecture Generated",
                    "phase": "Setup",
                    "estimated_hours": 1,
                    "status": "completed",
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actual_hours": 0.1
                }
            ],
            "time_spent": 0.1,
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "local_path": "C:\\Users\\mdsam\\OneDrive\\Desktop\\orbmech\\Backend\\EcommerceApp",
            "github_repo": "",
            "git_initialized": False,
            "tech_stack": {
                "frontend": "Vue",
                "backend": "Node.js", 
                "database": "MongoDB"
            },
            "features": ["authentication", "payment", "ecommerce", "full-stack"]
        }
        
        # Add to active projects
        data["active_projects"].append(enhanced_project)
        
        # Save back to file
        with open(projects_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("✅ Enhanced Vue Ecommerce project added to NEXUS database!")
        print(f"📛 Project Name: Enhanced Vue Ecommerce")
        print(f"🆔 Project ID: 28")
        print(f"📁 Project Path: C:\\Users\\mdsam\\OneDrive\\Desktop\\orbmech\\Backend\\EcommerceApp")
        print(f"📄 Files: 43 production-ready files")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding enhanced project: {e}")
        return False

if __name__ == "__main__":
    add_enhanced_project_to_nexus()