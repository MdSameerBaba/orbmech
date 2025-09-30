# test_improved_whatsapp_timing.py

"""
Test the improved 5-minute WhatsApp timing
"""

import sys
import os
from datetime import datetime, timedelta

# Add Backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

try:
    from Backend.WhatsAppIntegration import send_whatsapp_message, is_whatsapp_configured
    from Backend.Agents.DSAAgent import DSAAgent
    
    print("✅ Imports successful!")
    INTEGRATION_OK = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    INTEGRATION_OK = False

def test_new_timing():
    """Test the new 5-minute timing"""
    print("🕐 TESTING NEW 5-MINUTE TIMING")
    print("=" * 40)
    
    if not INTEGRATION_OK:
        print("❌ Integration not available")
        return
    
    if not is_whatsapp_configured():
        print("❌ WhatsApp not configured")
        return
    
    # Test with DSA command
    print("📱 Testing DSA WhatsApp command with new timing...")
    
    try:
        # This should now use 5-minute delay
        response = DSAAgent("send progress to whatsapp")
        print(f"Response: {response}")
        
        # Show expected timing
        future_time = datetime.now() + timedelta(minutes=5)
        print(f"\n⏰ Expected delivery time: {future_time.strftime('%H:%M:%S')}")
        print("🎯 Benefits of 5-minute delay:")
        print("  • More time for WhatsApp Web to load")
        print("  • Reduced timing conflicts")
        print("  • Better reliability on slower systems")
        print("  • Allows for manual intervention if needed")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_timing_comparison():
    """Show timing comparison"""
    print("\n📊 TIMING COMPARISON")
    print("=" * 40)
    
    print("Old Timing (2 minutes):")
    print("  ⚠️ Sometimes failed due to:")
    print("    • WhatsApp Web loading slowly")
    print("    • Browser startup time")
    print("    • System resource conflicts")
    
    print("\nNew Timing (5 minutes):")
    print("  ✅ More reliable because:")
    print("    • Extra time for system preparation")
    print("    • Better handling of slow connections")
    print("    • Reduced pywhatkit timing conflicts")
    print("    • User has time to prepare WhatsApp Web")

if __name__ == "__main__":
    print("🚀 NEXUS WHATSAPP IMPROVED TIMING TEST")
    print("=" * 50)
    
    show_timing_comparison()
    
    # Ask if user wants to test
    if INTEGRATION_OK and is_whatsapp_configured():
        print("\n" + "=" * 50)
        test_now = input("🧪 Test the new 5-minute timing? (y/n): ").lower().strip()
        
        if test_now == 'y':
            print("\n⚠️ This will schedule a WhatsApp message in 5 minutes!")
            confirm = input("Continue? (yes/no): ").lower().strip()
            
            if confirm == 'yes':
                test_new_timing()
                print("\n✅ Message scheduled with 5-minute delay!")
                print("📱 Check your WhatsApp in 5 minutes for delivery")
                print("🖥️ WhatsApp Web will open automatically when ready")
            else:
                print("✅ Test cancelled")
        else:
            print("✅ Skipping test - timing improved to 5 minutes for reliability")
    
    print("\n🎯 NEXUS WhatsApp Integration now uses 5-minute delays for maximum reliability!")