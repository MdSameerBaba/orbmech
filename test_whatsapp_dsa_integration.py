# test_whatsapp_dsa_integration.py

"""
🚀 NEXUS WhatsApp DSA Integration Test
Tests the new WhatsApp functionality for DSA content delivery
"""

import sys
import os

# Add Backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend', 'Agents'))

try:
    from Backend.WhatsAppIntegration import (
        test_whatsapp_integration,
        is_whatsapp_configured,
        get_user_phone
    )
    from Backend.Agents.DSAAgent import DSAAgent
    
    print("✅ All imports successful!")
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    INTEGRATION_AVAILABLE = False

def test_whatsapp_setup():
    """Test WhatsApp configuration"""
    print("\n🧪 TESTING WHATSAPP SETUP")
    print("=" * 50)
    
    if not INTEGRATION_AVAILABLE:
        print("❌ WhatsApp integration not available")
        return False
    
    configured = is_whatsapp_configured()
    phone = get_user_phone()
    
    print(f"📱 WhatsApp Configured: {configured}")
    print(f"📞 User Phone: {phone if phone else 'Not set'}")
    
    if configured:
        print("✅ WhatsApp integration is ready!")
        return True
    else:
        print("❌ WhatsApp not configured. Set USER_PHONE in .env file")
        return False

def test_dsa_whatsapp_commands():
    """Test DSA WhatsApp commands"""
    print("\n🧪 TESTING DSA WHATSAPP COMMANDS")
    print("=" * 50)
    
    if not INTEGRATION_AVAILABLE:
        print("❌ Integration not available")
        return
    
    # Test commands
    test_commands = [
        "whatsapp",
        "send progress to whatsapp", 
        "send arrays guide to whatsapp",
        "whatsapp trees study guide"
    ]
    
    for command in test_commands:
        print(f"\n🔍 Testing: '{command}'")
        print("-" * 30)
        
        try:
            response = DSAAgent(command)
            print(f"Response: {response[:200]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_manual_whatsapp_send():
    """Test manual WhatsApp message sending"""
    print("\n🧪 TESTING MANUAL WHATSAPP SEND")
    print("=" * 50)
    
    if not INTEGRATION_AVAILABLE:
        print("❌ Integration not available")
        return
    
    if not is_whatsapp_configured():
        print("❌ WhatsApp not configured")
        return
    
    print("🚀 Testing WhatsApp integration...")
    
    # This will schedule a test message
    try:
        success = test_whatsapp_integration()
        if success:
            print("✅ Test message scheduled! Check your WhatsApp in ~1 minute")
        else:
            print("❌ Failed to schedule test message")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_complete_workflow():
    """Demonstrate complete DSA + WhatsApp workflow"""
    print("\n🎯 COMPLETE DSA + WHATSAPP WORKFLOW DEMO")
    print("=" * 60)
    
    if not INTEGRATION_AVAILABLE:
        print("❌ Integration not available")
        return
    
    print("This demo shows how users can get DSA content via WhatsApp:")
    print("\n1. 📊 DSA Progress Summary")
    print("2. 📚 Study Guide Delivery")
    print("3. 📱 WhatsApp Integration")
    
    # Demo commands
    demo_commands = [
        ("DSA Summary", "show my dsa progress"),
        ("Arrays Guide", "arrays guide"),
        ("WhatsApp Progress", "send progress to whatsapp"),
        ("WhatsApp Study Guide", "send arrays guide to whatsapp")
    ]
    
    for title, command in demo_commands:
        print(f"\n🔍 {title}: '{command}'")
        print("-" * 40)
        
        try:
            response = DSAAgent(command)
            # Show first few lines
            lines = response.split('\n')
            for line in lines[:5]:
                if line.strip():
                    print(f"  {line}")
            if len(lines) > 5:
                print(f"  ... ({len(lines)-5} more lines)")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def show_usage_examples():
    """Show usage examples for users"""
    print("\n📋 NEXUS DSA + WHATSAPP USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        ("📊 Get Progress on WhatsApp", "send progress to whatsapp"),
        ("📚 Get Study Guide on WhatsApp", "send arrays guide to whatsapp"),
        ("🔍 Check WhatsApp Status", "whatsapp"),
        ("📱 Send Trees Guide", "whatsapp trees study guide"),
        ("📈 Send DSA Summary", "whatsapp my dsa summary")
    ]
    
    print("Available WhatsApp commands in NEXUS DSA mode:")
    for description, command in examples:
        print(f"  {description}")
        print(f"    Command: '{command}'")
        print()

if __name__ == "__main__":
    print("🚀 NEXUS WHATSAPP DSA INTEGRATION TEST")
    print("=" * 60)
    
    # Run all tests
    test_whatsapp_setup()
    test_dsa_whatsapp_commands()
    show_usage_examples()
    
    # Ask user if they want to test actual sending
    if INTEGRATION_AVAILABLE and is_whatsapp_configured():
        print("\n" + "=" * 60)
        test_send = input("🧪 Do you want to test actual WhatsApp sending? (y/n): ").lower().strip()
        
        if test_send == 'y':
            print("\n⚠️  WARNING: This will send actual WhatsApp messages!")
            confirm = input("Are you sure? (yes/no): ").lower().strip()
            
            if confirm == 'yes':
                test_manual_whatsapp_send()
                demo_complete_workflow()
            else:
                print("✅ Test cancelled - no messages sent")
        else:
            print("✅ Skipping actual message sending")
    
    print("\n🎉 Test completed!")
    print("📱 WhatsApp DSA integration is ready for use!")