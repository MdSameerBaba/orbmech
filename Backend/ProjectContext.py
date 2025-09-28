#!/usr/bin/env python3
"""
NEXUS Project Context Manager
Maintains current project state across sessions
"""

import json
import os
from datetime import datetime

CONTEXT_FILE = "Data/current_context.json"

def save_current_project_context(project_data):
    """Save current project context to file"""
    try:
        context = {
            "current_project": project_data,
            "last_updated": datetime.now().isoformat(),
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        # Ensure Data directory exists
        os.makedirs("Data", exist_ok=True)
        
        with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error saving project context: {e}")
        return False

def load_current_project_context():
    """Load current project context from file"""
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
                context = json.load(f)
                return context.get("current_project", None)
    except Exception as e:
        print(f"⚠️ Error loading project context: {e}")
    return None

def clear_current_project_context():
    """Clear current project context"""
    try:
        if os.path.exists(CONTEXT_FILE):
            os.remove(CONTEXT_FILE)
        return True
    except Exception as e:
        print(f"❌ Error clearing project context: {e}")
        return False

def get_current_project_path():
    """Get current project's local path"""
    project = load_current_project_context()
    if project:
        return project.get("local_path", "")
    return ""

def is_project_context_active():
    """Check if there's an active project context"""
    return load_current_project_context() is not None