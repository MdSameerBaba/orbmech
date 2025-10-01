#!/usr/bin/env python3
"""
Launch NEXUS Modern Web Interface
Ultra-professional web-based GUI with glassmorphism design
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def install_requirements():
    """Install required packages for web interface"""
    requirements = [
        'flask==2.3.3',
        'flask-socketio==5.3.6',
        'python-socketio==5.8.0',
        'eventlet==0.33.3'
    ]
    
    print("🔧 Installing web interface requirements...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ Installed: {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {req}")
    print("✅ Requirements installation complete!")

def launch_modern_web_nexus():
    """Launch the modern web interface"""
    
    print("\n" + "="*60)
    print("🚀 NEXUS MODERN WEB INTERFACE LAUNCHER")
    print("="*60)
    print("🎨 Ultra-Modern Glassmorphism Design")
    print("📱 Mobile Responsive Interface")
    print("🔊 Full Audio-Visual Integration")
    print("⚡ Real-time WebSocket Communication")
    print("🎤 Advanced Voice Recognition")
    print("="*60)
    
    # Set up paths
    interface_dir = Path(__file__).parent / "Interface"
    web_interface_path = interface_dir / "ModernWebInterface.py"
    
    if not web_interface_path.exists():
        print("❌ Web interface file not found!")
        return False
    
    # Install requirements
    install_requirements()
    
    # Launch web interface
    print("\n🌐 Starting NEXUS Web Server...")
    
    try:
        # Add interface directory to Python path
        sys.path.insert(0, str(interface_dir))
        
        # Import and launch web interface
        from ModernWebInterface import launch_modern_web_interface
        
        # Open browser automatically
        def open_browser():
            time.sleep(2)  # Wait for server to start
            webbrowser.open('http://127.0.0.1:5000')
            print("🌍 Browser opened automatically!")
        
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Launch the interface
        print("🚀 Launching Modern Web Interface...")
        launch_modern_web_interface(host='127.0.0.1', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Web interface stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error launching web interface: {e}")
        print("\nTroubleshooting:")
        print("1. Check if all requirements are installed")
        print("2. Ensure port 5000 is available")
        print("3. Check firewall settings")
        return False

if __name__ == "__main__":
    try:
        success = launch_modern_web_nexus()
        if success:
            print("\n✅ NEXUS Web Interface session completed successfully!")
        else:
            print("\n❌ NEXUS Web Interface encountered errors")
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
    
    input("\nPress Enter to exit...")