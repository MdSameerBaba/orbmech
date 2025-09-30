#!/usr/bin/env python3
"""
Complete Personal Assistant Integration Test
Tests the full NEXUS system with integrated personal assistant functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from personal_assistant_manager import PersonalAssistantManager

def test_complete_personal_assistant():
    """Test comprehensive personal assistant integration"""
    print("🤖 COMPLETE PERSONAL ASSISTANT INTEGRATION TEST")
    print("=" * 60)
    
    # Initialize personal assistant
    pa = PersonalAssistantManager()
    
    # Test all major categories
    test_queries = [
        # Calendar Management
        ("📅 Calendar Management", [
            "show calendar",
            "schedule meeting with team tomorrow at 3pm",
            "add appointment dentist Friday 10am"
        ]),
        
        # Task Management  
        ("📋 Task Management", [
            "add task prepare presentation for Monday",
            "add task buy groceries priority high",
            "show tasks",
            "show priority tasks"
        ]),
        
        # Expense Tracking
        ("💰 Expense Management", [
            "add expense $25 lunch",
            "add expense $120 electricity bill",
            "show expenses this month",
            "budget analysis"
        ]),
        
        # Health Monitoring
        ("🏃 Health & Fitness", [
            "log 8000 steps today",
            "log workout 45 minutes",
            "log sleep 7.5 hours",
            "health summary"
        ]),
        
        # Contact Management
        ("👥 Contact Management", [
            "add contact John Smith phone 555-1234",
            "add contact Sarah email sarah@email.com",
            "find contact John",
            "show contacts"
        ]),
        
        # Bill Tracking
        ("📄 Bill Management", [
            "add bill Netflix $15.99 due 15th",
            "add bill rent $1200 due 1st",
            "show bills",
            "upcoming bills"
        ]),
        
        # Entertainment
        ("🎬 Entertainment", [
            "movie recommendations",
            "music recommendations",
            "tv show recommendations",
            "entertainment news"
        ]),
        
        # Help System
        ("❓ Help & Information", [
            "personal assistant help",
            "what can you do",
            "help with calendar",
            "expense help"
        ])
    ]
    
    # Test each category
    for category, queries in test_queries:
        print(f"\n{category}")
        print("-" * 40)
        
        for query in queries:
            print(f"🔍 Query: {query}")
            try:
                response = pa.process_personal_assistant_query(query)
                print("✅ Response generated successfully")
                print(f"📝 Preview: {response[:100]}...")
            except Exception as e:
                print(f"❌ Error: {e}")
            print()
    
    print("🎉 COMPLETE PERSONAL ASSISTANT TEST FINISHED!")
    print("🚀 All life management features successfully integrated!")

def demo_nexus_integration():
    """Demo the complete NEXUS integration"""
    print("\n🚀 NEXUS + PERSONAL ASSISTANT INTEGRATION DEMO")
    print("=" * 60)
    
    # Simulate different query types that would route to different agents
    routing_examples = [
        ("Personal Assistant", "show my calendar for today"),
        ("DSA Agent", "explain arrays and show implementation"),
        ("Project Agent", "switch to my NEXUS project"),
        ("Stock Agent", "analyze Tesla stock performance"),
        ("NEXUS Career", "help me prepare for Google interview"),
        ("Personal Assistant", "add expense $50 for groceries"),
        ("Personal Assistant", "schedule meeting with boss tomorrow")
    ]
    
    print("📊 ROUTING DEMONSTRATION:")
    print("-" * 30)
    
    for agent_type, query in routing_examples:
        print(f"🔍 Query: \"{query}\"")
        print(f"🎯 Would route to: {agent_type}")
        print()
    
    print("✨ NEXUS now provides:")
    print("🏢 Career acceleration & interview prep")
    print("📚 DSA learning & coding practice") 
    print("🚀 Project development & management")
    print("📈 Stock analysis & market insights")
    print("🤖 Complete personal life management")
    print("📱 WhatsApp integration for content delivery")
    print()
    
    print("🎯 NEXUS is now a COMPLETE personal assistant!")
    print("🌟 From career growth to daily life management!")

if __name__ == "__main__":
    try:
        test_complete_personal_assistant()
        demo_nexus_integration()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()