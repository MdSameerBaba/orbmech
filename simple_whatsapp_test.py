# simple_whatsapp_test.py

"""
Simple WhatsApp test with longer delay and better error handling
"""

import pywhatkit as kit
from datetime import datetime, timedelta

def send_simple_test():
    phone = "+919133520043"
    message = "Hello from NEXUS! 🚀"
    
    # 5 minute delay for safety
    future_time = datetime.now() + timedelta(minutes=5)
    hour = future_time.hour
    minute = future_time.minute
    
    print(f"📱 Sending to: {phone}")
    print(f"⏰ Scheduled for: {hour:02d}:{minute:02d}")
    print(f"💬 Message: {message}")
    
    try:
        kit.sendwhatmsg(phone, message, hour, minute, wait_time=30, tab_close=False)
        print("✅ Message scheduled successfully!")
        print("🔍 Note: tab_close=False so you can see what happens")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Simple WhatsApp Test")
    print("=" * 30)
    send_simple_test()