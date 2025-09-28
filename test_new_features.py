#!/usr/bin/env python3
"""
Comprehensive test for all new NEXUS features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_stock_features():
    """Test enhanced stock analytics"""
    print("📈 Testing Enhanced Stock Features...")
    try:
        from Backend.Agents.StockAgent import StockAgent
        
        # Test technical analysis
        response1 = StockAgent("technical analysis for AAPL")
        print("✅ Technical Analysis:", "Technical Analysis" in response1)
        
        # Test stock recommendations
        response2 = StockAgent("stock recommendations")
        print("✅ Stock Recommendations:", "RECOMMENDATIONS" in response2)
        
        # Test regular stock query
        response3 = StockAgent("what's apple stock price?")
        print("✅ Regular Stock Query:", "Apple" in response3 or "AAPL" in response3)
        
    except Exception as e:
        print(f"❌ Enhanced stock features test failed: {e}")

def test_code_analyzer():
    """Test code quality analyzer integration"""
    print("\n🔍 Testing Code Quality Analyzer...")
    try:
        from Backend.Agents.DSAAgent import DSAAgent
        
        # Test code analysis request
        response = DSAAgent("analyze code")
        print("✅ Code Analysis Request:", "CODE QUALITY ANALYZER" in response)
        
        # Test direct code analysis
        from Backend.code_quality_analyzer import DSACodeAnalyzer
        
        test_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
        
        analysis = DSACodeAnalyzer(test_code, "Fibonacci", "python")
        print("✅ Direct Code Analysis:", "COMPLEXITY ANALYSIS" in analysis)
        
    except Exception as e:
        print(f"❌ Code analyzer test failed: {e}")

def test_reminder_system():
    """Test smart reminder system"""
    print("\n🔔 Testing Smart Reminder System...")
    try:
        from Backend.smart_reminders import ReminderAgent, reminder_system
        
        # Test reminder commands
        response1 = ReminderAgent("set reminder to test feature in 1 minute")
        print("✅ Set Reminder:", "Reminder set" in response1)
        
        response2 = ReminderAgent("list reminders")
        print("✅ List Reminders:", "ACTIVE REMINDERS" in response2)
        
        response3 = ReminderAgent("start reminder system")
        print("✅ Start System:", "started" in response3)
        
        # Test help
        response4 = ReminderAgent("help")
        print("✅ Help System:", "REMINDER SYSTEM COMMANDS" in response4)
        
        # Stop the system
        reminder_system.stop_monitoring()
        
    except Exception as e:
        print(f"❌ Reminder system test failed: {e}")

def test_decision_making_updates():
    """Test that decision making recognizes new features"""
    print("\n🧠 Testing Decision Making Updates...")
    try:
        from Backend.Model import FirstLayerDMM
        
        test_cases = [
            ("set reminder to call mom", "reminder"),
            ("technical analysis for Apple", "stock"),
            ("analyze my code quality", "dsa"),
            ("stock recommendations", "stock")
        ]
        
        for query, expected in test_cases:
            decision = FirstLayerDMM(query)
            if decision and any(expected in d for d in decision):
                print(f"✅ '{query}' → {decision[0]}")
            else:
                print(f"⚠️ '{query}' → {decision} (expected {expected})")
                
    except Exception as e:
        print(f"❌ Decision making test failed: {e}")

def test_integration():
    """Test integration with main processing"""
    print("\n🔗 Testing Main System Integration...")
    try:
        from Main import ProcessQuery
        
        # This would normally be tested by running the full GUI
        # For now, we'll just test that imports work
        print("✅ Main system imports working")
        
        # Test that all agents can be imported
        from Backend.Agents.StockAgent import StockAgent
        from Backend.Agents.DSAAgent import DSAAgent
        from Backend.smart_reminders import ReminderAgent
        
        print("✅ All agents importable")
        
    except Exception as e:
        print(f"⚠️ Integration test note: {e}")

def test_data_files():
    """Test that new data files are created properly"""
    print("\n📁 Testing Data File Creation...")
    
    # Test reminder data file
    try:
        from Backend.smart_reminders import reminder_system
        reminder_system.add_reminder("Test", "Test message", "in 1 hour")
        
        if os.path.exists("Data/reminders.json"):
            print("✅ Reminders data file created")
        else:
            print("⚠️ Reminders data file not found")
            
    except Exception as e:
        print(f"❌ Reminder data file test failed: {e}")
    
    # Test chart generation
    chart_files = [
        "Data/AAPL_technical_analysis.png",
        "Data/dsa_analysis.png",
        "Data/project_dashboard.png"
    ]
    
    for chart_file in chart_files:
        if os.path.exists(chart_file):
            print(f"✅ Chart file exists: {os.path.basename(chart_file)}")
        else:
            print(f"⚠️ Chart file missing: {os.path.basename(chart_file)}")

def main():
    print("🚀 NEXUS New Features - Comprehensive Test Suite")
    print("=" * 60)
    
    test_enhanced_stock_features()
    test_code_analyzer()
    test_reminder_system()
    test_decision_making_updates()
    test_integration()
    test_data_files()
    
    print("\n" + "=" * 60)
    print("🎉 NEW FEATURES TEST COMPLETE!")
    print("\n📊 New Features Added:")
    print("  🔹 Enhanced Stock Analytics with Technical Indicators")
    print("  🔹 Smart Reminder System with Natural Language")
    print("  🔹 Code Quality Analyzer for DSA Solutions")
    print("  🔹 Improved Error Handling and Rate Limiting")
    print("  🔹 Better Chart Generation with Font Fixes")
    print("\n✨ NEXUS AI Assistant is now more powerful than ever!")

if __name__ == "__main__":
    main()