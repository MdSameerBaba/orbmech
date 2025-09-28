#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup System Modes for OrbMech
Initializes all available modes with their configurations
"""

import json
import os

def setup_system_modes():
    """Initialize system modes configuration"""
    
    mode_config = {
        "current_mode": "general",
        "available_modes": {
            "general": {
                "description": "General AI assistant for conversations and basic tasks",
                "commands": ["chat", "ask questions", "general help", "automation tasks"]
            },
            "stock": {
                "description": "Stock market analysis and portfolio management",
                "commands": ["portfolio analysis", "stock prices", "market trends", "investment advice"]
            },
            "dsa": {
                "description": "Data Structures & Algorithms practice and learning",
                "commands": ["coding problems", "algorithm help", "leetcode tracking", "study guides"]
            },
            "project": {
                "description": "Project management with Git integration for active development",
                "commands": ["git operations", "project tracking", "progress monitoring", "github integration"]
            }
        }
    }
    
    # Ensure Data directory exists
    os.makedirs("Data", exist_ok=True)
    
    # Save mode configuration
    with open(r"Data\system_mode.json", 'w', encoding='utf-8') as f:
        json.dump(mode_config, f, indent=2)
    
    print("System modes initialized successfully!")
    print("\nAvailable modes:")
    for mode, details in mode_config["available_modes"].items():
        print(f"  {mode.upper()}: {details['description']}")
    
    print(f"\nCurrent mode: {mode_config['current_mode'].upper()}")
    print("\nSwitch modes using: 'project mode', 'stock mode', 'dsa mode', 'general mode'")

if __name__ == "__main__":
    setup_system_modes()