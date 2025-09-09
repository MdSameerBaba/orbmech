import json
import os

MODE_FILE = r"Data\system_mode.json"

def load_system_mode():
    """Load current system mode"""
    try:
        with open(MODE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"current_mode": "general", "available_modes": {}}

def save_system_mode(mode_data):
    """Save system mode configuration"""
    try:
        with open(MODE_FILE, 'w', encoding='utf-8') as f:
            json.dump(mode_data, f, indent=2)
        return True
    except IOError as e:
        print(f"❌ Error saving system mode: {e}")
        return False

def get_current_mode():
    """Get the current active mode"""
    mode_data = load_system_mode()
    return mode_data.get("current_mode", "general")

def switch_mode(new_mode):
    """Switch to a new mode"""
    mode_data = load_system_mode()
    available_modes = mode_data.get("available_modes", {})
    
    if new_mode in available_modes:
        mode_data["current_mode"] = new_mode
        if save_system_mode(mode_data):
            return f"✅ Switched to {new_mode.upper()} mode! {available_modes[new_mode]['description']}"
        else:
            return "❌ Failed to switch mode."
    else:
        available = ", ".join(available_modes.keys())
        return f"❌ Invalid mode '{new_mode}'. Available modes: {available}"

def get_mode_info():
    """Get information about all available modes"""
    mode_data = load_system_mode()
    current = mode_data.get("current_mode", "general")
    modes = mode_data.get("available_modes", {})
    
    info = f"🔧 SYSTEM MODES\n\nCurrent Mode: {current.upper()}\n\n"
    
    for mode, details in modes.items():
        status = "🟢 ACTIVE" if mode == current else "⚪ Available"
        info += f"{status} {mode.upper()}: {details['description']}\n"
        info += f"   Commands: {', '.join(details['commands'])}\n\n"
    
    info += "💡 Switch modes: 'stock mode', 'dsa mode', 'general mode'"
    return info

def should_route_to_mode(query, decision):
    """Check if query should be routed based on current mode"""
    current_mode = get_current_mode()
    
    # If in stock mode, route stock-related queries directly
    if current_mode == "stock" and not any(d.startswith(("mode", "exit")) for d in decision):
        return "stock", query
    
    # If in DSA mode, route DSA-related queries directly  
    if current_mode == "dsa" and not any(d.startswith(("mode", "exit")) for d in decision):
        return "dsa", query
    
    # If in project mode, route project-related queries directly
    if current_mode == "project" and not any(d.startswith(("mode", "exit")) for d in decision):
        return "project", query
    
    # Otherwise, use normal routing
    return None, None