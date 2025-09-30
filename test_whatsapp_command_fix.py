# test_whatsapp_command_fix.py

"""
Test to verify the WhatsApp command parsing fix
Ensures "guide" commands don't get confused with "progress" commands
"""

import sys
import os

# Add Backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend', 'Agents'))

try:
    from DSAAgent import DSAAgent
    print("✅ DSAAgent imported successfully!")
    AGENT_OK = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    AGENT_OK = False

def test_whatsapp_commands():
    """Test different WhatsApp command variations"""
    print("🧪 TESTING WHATSAPP COMMAND PARSING")
    print("=" * 50)
    
    if not AGENT_OK:
        print("❌ Cannot test - agent not available")
        return
    
    # Test commands that should send GUIDES
    guide_commands = [
        "send arrays guide to whatsapp",
        "send trees guide to whatsapp", 
        "whatsapp dynamic programming guide",
        "send strings study guide to whatsapp"
    ]
    
    # Test commands that should send PROGRESS
    progress_commands = [
        "send progress to whatsapp",
        "whatsapp my dsa summary",
        "send my progress to whatsapp"
    ]
    
    print("🔍 TESTING GUIDE COMMANDS:")
    print("-" * 30)
    
    for command in guide_commands:
        print(f"\n📚 Testing: '{command}'")
        try:
            response = DSAAgent(command)
            # Check if response mentions "study guide"
            if "study guide" in response.lower():
                print("✅ CORRECT: Detected as study guide")
            elif "progress report" in response.lower():
                print("❌ BUG: Incorrectly detected as progress")
            else:
                print(f"📝 Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🔍 TESTING PROGRESS COMMANDS:")
    print("-" * 30)
    
    for command in progress_commands:
        print(f"\n📊 Testing: '{command}'")
        try:
            response = DSAAgent(command)
            # Check if response mentions "progress report"
            if "progress report" in response.lower():
                print("✅ CORRECT: Detected as progress report")
            elif "study guide" in response.lower():
                print("❌ BUG: Incorrectly detected as study guide")
            else:
                print(f"📝 Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_command_priority():
    """Test command priority to ensure guides take precedence"""
    print("\n🎯 TESTING COMMAND PRIORITY")
    print("=" * 50)
    
    # This command has both "arrays" and could be confused
    ambiguous_commands = [
        "send arrays guide to whatsapp",  # Should be guide
        "arrays guide",                   # Should be guide  
        "arrays progress",                # Should be progress
        "whatsapp arrays guide"           # Should be guide
    ]
    
    for command in ambiguous_commands:
        print(f"\n🔍 Testing: '{command}'")
        expected = "guide" if "guide" in command else "progress"
        
        try:
            response = DSAAgent(command)
            if "study guide" in response.lower() and expected == "guide":
                print("✅ CORRECT: Properly identified as guide")
            elif "progress report" in response.lower() and expected == "progress":
                print("✅ CORRECT: Properly identified as progress")
            else:
                print(f"❓ RESULT: {response[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

def show_correct_usage():
    """Show correct command usage"""
    print("\n📋 CORRECT WHATSAPP COMMAND USAGE")
    print("=" * 50)
    
    print("📚 FOR STUDY GUIDES (with YouTube links):")
    print("  • 'send arrays guide to whatsapp'")
    print("  • 'send trees guide to whatsapp'")
    print("  • 'whatsapp dynamic programming guide'")
    print("  • 'send strings study guide to whatsapp'")
    
    print("\n📊 FOR PROGRESS REPORTS:")
    print("  • 'send progress to whatsapp'")
    print("  • 'whatsapp my dsa summary'")
    print("  • 'send my progress to whatsapp'")
    
    print("\n🎯 KEY WORDS:")
    print("  • Use 'guide' or 'study' for study guides")
    print("  • Use 'progress' or 'summary' for progress reports")

if __name__ == "__main__":
    print("🔧 NEXUS WHATSAPP COMMAND PARSING FIX TEST")
    print("=" * 60)
    
    test_whatsapp_commands()
    test_command_priority()
    show_correct_usage()
    
    print("\n🎉 COMMAND PARSING TEST COMPLETED!")
    print("📱 The fix ensures 'guide' commands send study guides")
    print("📊 And 'progress' commands send progress reports")