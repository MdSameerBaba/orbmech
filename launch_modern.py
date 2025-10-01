#!/usr/bin/env python3
"""
NEXUS Modern GUI Launcher
Simple launcher script for the modern NEXUS interface
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 NEXUS Modern Interface Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    if not (current_dir / "ModernMain.py").exists():
        print("❌ Error: Please run this script from the NEXUS root directory")
        print(f"Current directory: {current_dir}")
        return
    
    print("✅ NEXUS directory detected")
    print("🎨 Launching modern interface...")
    
    try:
        # Launch the modern GUI
        subprocess.run([sys.executable, "ModernMain.py", "--modern"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching modern GUI: {e}")
        print("🔄 Falling back to classic interface...")
        try:
            subprocess.run([sys.executable, "Main.py"], check=True)
        except subprocess.CalledProcessError as e2:
            print(f"❌ Error launching classic GUI: {e2}")
    except KeyboardInterrupt:
        print("\n👋 NEXUS interface closed by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()