# debug_whatsapp_issue.py

"""
🔍 WhatsApp Delivery Debug Script
Helps identify why WhatsApp messages aren't being delivered
"""

import sys
import os
from datetime import datetime, timedelta

# Add Backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

try:
    from Backend.WhatsAppIntegration import (
        send_whatsapp_message,
        is_whatsapp_configured,
        get_user_phone,
        format_dsa_progress_message
    )
    import pywhatkit as kit
    from dotenv import dotenv_values
    
    print("✅ All imports successful!")
    IMPORTS_OK = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    IMPORTS_OK = False

def check_configuration():
    """Check WhatsApp configuration"""
    print("\n🔧 CHECKING WHATSAPP CONFIGURATION")
    print("=" * 50)
    
    # Check .env file
    env_vars = dotenv_values(".env")
    user_phone = env_vars.get("USER_PHONE", "")
    
    print(f"📁 .env file USER_PHONE: {user_phone}")
    print(f"📱 WhatsApp configured: {is_whatsapp_configured()}")
    print(f"📞 Phone from function: {get_user_phone()}")
    
    # Validate phone number format
    if user_phone:
        if user_phone.startswith("+"):
            print("✅ Phone number has country code")
        else:
            print("❌ Phone number missing country code (+)")
        
        if len(user_phone) >= 10:
            print("✅ Phone number length looks good")
        else:
            print("❌ Phone number might be too short")
    else:
        print("❌ No phone number found in .env")
    
    return user_phone

def test_pywhatkit_directly():
    """Test pywhatkit directly with simple message"""
    print("\n🧪 TESTING PYWHATKIT DIRECTLY")
    print("=" * 50)
    
    user_phone = check_configuration()
    
    if not user_phone:
        print("❌ Cannot test - no phone number configured")
        return False
    
    # Calculate send time (3 minutes from now)
    future_time = datetime.now() + timedelta(minutes=3)
    hour = future_time.hour
    minute = future_time.minute
    
    test_message = "🧪 NEXUS WhatsApp Test Message\n\nThis is a direct test of pywhatkit functionality.\n\nIf you receive this, the integration is working!"
    
    print(f"📱 Testing with phone: {user_phone}")
    print(f"⏰ Scheduled time: {hour:02d}:{minute:02d}")
    print(f"📝 Message length: {len(test_message)} characters")
    
    try:
        print("\n🚀 Attempting to schedule message...")
        kit.sendwhatmsg(user_phone, test_message, hour, minute, wait_time=20, tab_close=True)
        print("✅ Message scheduled successfully!")
        print("📱 WhatsApp Web should open automatically")
        print("⏰ Message will be sent in ~3 minutes")
        return True
        
    except Exception as e:
        print(f"❌ Error scheduling message: {e}")
        print("\n🔍 Common issues:")
        print("• WhatsApp Web not logged in")
        print("• Chrome/Browser not available")
        print("• Phone number format incorrect")
        print("• System time/timezone issues")
        return False

def check_system_requirements():
    """Check system requirements for pywhatkit"""
    print("\n🖥️ CHECKING SYSTEM REQUIREMENTS")
    print("=" * 50)
    
    # Check if Chrome/browser is available
    import webbrowser
    try:
        print("🌐 Testing browser availability...")
        # Don't actually open, just test
        print("✅ Browser access available")
    except Exception as e:
        print(f"❌ Browser issue: {e}")
    
    # Check pywhatkit version
    try:
        print(f"📦 pywhatkit version: {kit.__version__ if hasattr(kit, '__version__') else 'Unknown'}")
    except:
        print("⚠️ Could not determine pywhatkit version")
    
    # Check current time
    now = datetime.now()
    print(f"🕐 Current time: {now.strftime('%H:%M:%S')}")
    print(f"📅 Current date: {now.strftime('%Y-%m-%d')}")

def show_troubleshooting_steps():
    """Show troubleshooting steps"""
    print("\n🛠️ TROUBLESHOOTING STEPS")
    print("=" * 50)
    
    print("""
1. 🌐 **WhatsApp Web Setup:**
   • Open https://web.whatsapp.com in Chrome
   • Scan QR code with your phone
   • Ensure you stay logged in
   
2. 📱 **Phone Number Format:**
   • Must include country code: +919133520043
   • No spaces or special characters
   • Example: +1234567890 (US), +919876543210 (India)
   
3. ⏰ **Timing Issues:**
   • pywhatkit needs 2+ minutes delay
   • System time must be accurate
   • Check timezone settings
   
4. 🌐 **Browser Requirements:**
   • Chrome browser installed
   • WhatsApp Web permissions granted
   • No popup blockers interfering
   
5. 🔧 **Alternative Testing:**
   • Try manual WhatsApp Web first
   • Test with longer delay (5+ minutes)
   • Check if messages appear in "Sent" folder
   
6. 📞 **Phone Number Verification:**
   • Ensure number is correct and active
   • Test with different number format
   • Verify country code is correct
""")

def manual_test_suggestion():
    """Suggest manual testing approach"""
    print("\n💡 MANUAL TEST SUGGESTION")
    print("=" * 50)
    
    user_phone = get_user_phone()
    future_time = datetime.now() + timedelta(minutes=5)
    
    print(f"""
Try this manual test in Python console:

```python
import pywhatkit as kit
from datetime import datetime, timedelta

# Your phone number
phone = "{user_phone}"

# 5 minutes from now
future = datetime.now() + timedelta(minutes=5)
hour = future.hour
minute = future.minute

# Simple test message
message = "Test from NEXUS"

# Send message
kit.sendwhatmsg(phone, message, hour, minute, wait_time=25, tab_close=True)
```

Expected behavior:
1. Chrome opens WhatsApp Web
2. WhatsApp Web loads (if logged in)
3. Message typed automatically after wait time
4. Message sent automatically
5. Browser closes (if tab_close=True)
""")

if __name__ == "__main__":
    print("🔍 NEXUS WHATSAPP DELIVERY DEBUG")
    print("=" * 60)
    
    if not IMPORTS_OK:
        print("❌ Cannot proceed - import errors")
        exit(1)
    
    # Run all checks
    check_configuration()
    check_system_requirements()
    show_troubleshooting_steps()
    
    # Ask if user wants to test
    print("\n" + "=" * 60)
    test_now = input("🧪 Do you want to test direct pywhatkit sending? (y/n): ").lower().strip()
    
    if test_now == 'y':
        print("\n⚠️ This will schedule a real WhatsApp message in 3 minutes!")
        confirm = input("Continue? (yes/no): ").lower().strip()
        
        if confirm == 'yes':
            success = test_pywhatkit_directly()
            if success:
                print("\n✅ Test scheduled! Check your WhatsApp in 3 minutes.")
                print("🖥️ Watch for Chrome/WhatsApp Web to open automatically.")
            else:
                print("\n❌ Test failed. Check the troubleshooting steps above.")
        else:
            print("✅ Test cancelled")
    else:
        manual_test_suggestion()
    
    print("\n🎯 If issues persist:")
    print("1. Try WhatsApp Web login first: https://web.whatsapp.com")
    print("2. Increase delay time to 5+ minutes")
    print("3. Check Chrome browser permissions")
    print("4. Verify phone number format with country code")