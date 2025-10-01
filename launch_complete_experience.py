#!/usr/bin/env python3
"""
NEXUS Complete Modern Experience Launcher
Comprehensive launcher showcasing all enhanced features with graphics and audio
"""

import sys
import os
import time
from datetime import datetime

def display_welcome_banner():
    """Display an enhanced welcome banner"""
    print("\n" + "="*80)
    print("🤖  NEXUS - Complete AI Personal Assistant  🤖")
    print("="*80)
    print("🎨  MODERN GUI EXPERIENCE with Enhanced Features")
    print("-"*80)
    print("✨  NEW FEATURES INCLUDED:")
    print("   🎬  Animated Jarvis Assistant (Graphics/Jarvis.gif)")
    print("   🔊  Sound Effects (Graphics/activate.wav)")
    print("   🎨  Custom Window Controls (Minimize/Maximize/Close.png)")
    print("   🎤  Enhanced Voice Control (Mic_on/Mic_off.png)")
    print("   💫  Glassmorphism Design with Smooth Animations")
    print("   🏠  Interactive Dashboard with Real-time Updates")
    print("   🤖  Complete Personal Assistant Interface")
    print("   ⚡  Smart Quick Actions with Visual Feedback")
    print("-"*80)
    print(f"📅  Launch Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

def check_graphics_assets():
    """Check if graphics assets are available"""
    graphics_path = os.path.join(os.path.dirname(__file__), "Interface", "Graphics")
    
    assets = {
        "Jarvis.gif": "🎬 Animated Assistant",
        "activate.wav": "🔊 Activation Sound",
        "Mic_on.png": "🎤 Voice Control (On)",
        "Mic_off.png": "🎤 Voice Control (Off)",
        "Close.png": "❌ Close Button",
        "Minimize.png": "➖ Minimize Button",
        "Maximize.png": "⬜ Maximize Button",
        "Home.png": "🏠 Home Icon",
        "Settings.png": "⚙️ Settings Icon",
        "Send.png": "📤 Send Icon"
    }
    
    print("\n🔍  GRAPHICS ASSETS STATUS:")
    print("-"*50)
    
    all_found = True
    for asset, description in assets.items():
        asset_path = os.path.join(graphics_path, asset)
        if os.path.exists(asset_path):
            print(f"✅  {description}")
        else:
            print(f"❌  {description} - NOT FOUND")
            all_found = False
    
    print("-"*50)
    if all_found:
        print("🎉  All graphics assets found! Full experience available.")
    else:
        print("⚠️   Some assets missing, but GUI will use fallbacks.")
    
    return all_found

def launch_modern_nexus():
    """Launch the modern NEXUS experience"""
    print("\n🚀  LAUNCHING NEXUS MODERN EXPERIENCE...")
    print("-"*50)
    
    try:
        # Import and launch
        os.system("python ModernMain.py --modern")
        
    except KeyboardInterrupt:
        print("\n\n👋  NEXUS Shutdown Complete")
        print("    Thank you for using NEXUS AI Assistant!")
        
    except Exception as e:
        print(f"\n❌  Error launching NEXUS: {e}")
        print("    Please check your installation and try again.")

def show_feature_guide():
    """Show a quick feature guide"""
    print("\n📖  QUICK FEATURE GUIDE:")
    print("-"*50)
    print("🏠  Dashboard Tab:")
    print("    • View real-time statistics and insights")
    print("    • Interactive widgets with hover effects")
    print("    • Quick action buttons with sound feedback")
    print()
    print("💬  Chat Tab:")
    print("    • Modern chat interface with NEXUS")
    print("    • Enhanced voice control with Jarvis animation")
    print("    • Sound effects for voice activation")
    print()
    print("🤖  Assistant Tab:")
    print("    • Complete personal life management")
    print("    • Calendar, tasks, expenses, health tracking")
    print("    • Contact management and entertainment")
    print()
    print("📊  Analytics Tab:")
    print("    • Comprehensive data visualization")
    print("    • Performance metrics and trends")
    print("    • Insights and recommendations")
    print("-"*50)
    print("💡  TIP: Try clicking the microphone button for voice control!")

def main():
    """Main launcher function"""
    try:
        # Clear screen (works on both Windows and Unix)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display welcome
        display_welcome_banner()
        
        # Check assets
        assets_available = check_graphics_assets()
        
        # Show feature guide
        show_feature_guide()
        
        # Confirmation prompt
        print("\n" + "="*80)
        response = input("🎯  Ready to launch NEXUS Modern Experience? (Y/n): ").strip().lower()
        
        if response in ['', 'y', 'yes']:
            launch_modern_nexus()
        else:
            print("\n👋  Launch cancelled. Run this script again when ready!")
            
    except KeyboardInterrupt:
        print("\n\n👋  Launcher interrupted. Goodbye!")
        
    except Exception as e:
        print(f"\n❌  Launcher error: {e}")

if __name__ == "__main__":
    main()