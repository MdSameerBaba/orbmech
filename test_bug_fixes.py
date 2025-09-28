#!/usr/bin/env python3
"""
Test the fixes we made to NEXUS AI Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import warnings

# Suppress font warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*missing from font.*")
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']

def test_stock_fixes():
    """Test the stock rate limiting fixes"""
    print("📈 Testing Stock Rate Limiting Fixes...")
    try:
        from Backend.Agents.StockAgent import get_stock_price, StockAgent
        
        # Test individual stock prices with rate limit handling
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        for symbol in symbols:
            price = get_stock_price(symbol)
            if price:
                print(f"✅ {symbol}: ${price:.2f}")
            else:
                print(f"⚠️ Could not get {symbol} price")
        
        # Test stock agent
        response = StockAgent("What's Apple stock price?")
        if response and "Apple" in response:
            print("✅ Stock agent responding correctly")
        else:
            print("⚠️ Stock agent response unclear")
            
    except Exception as e:
        print(f"❌ Stock test failed: {e}")

def test_project_fixes():
    """Test project deadline fixes"""
    print("\n📊 Testing Project Deadline Fixes...")
    try:
        from Backend.Agents.ProjectAgent import ProjectAgent
        
        # Test project listing
        response = ProjectAgent("show all projects")
        if "days left" in response and not "-" in response:
            print("✅ Project deadlines fixed")
        else:
            print("⚠️ Some projects may still have past deadlines")
            print(f"Response sample: {response[:200]}...")
            
    except Exception as e:
        print(f"❌ Project test failed: {e}")

def test_font_warnings():
    """Test that font warnings are suppressed"""
    print("\n🔤 Testing Font Warning Suppression...")
    try:
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # Generate a chart that would normally trigger font warnings
            from Backend.Agents.DSAAgent import DSAAgent
            response = DSAAgent("show my progress")
            
            # Check if any font warnings were raised
            font_warnings = [warning for warning in w if "missing from font" in str(warning.message)]
            
            if len(font_warnings) == 0:
                print("✅ Font warnings successfully suppressed")
            else:
                print(f"⚠️ {len(font_warnings)} font warnings still present")
                
    except Exception as e:
        print(f"❌ Font warning test failed: {e}")

def test_decision_making():
    """Test decision making is still working correctly"""
    print("\n🧠 Testing Decision Making...")
    try:
        from Backend.Model import FirstLayerDMM
        
        test_cases = [
            ("what's apple stock price?", "stock"),
            ("arrays guide", "dsa"),
            ("create project MyApp", "project"),
            ("tell me a joke", "general")
        ]
        
        for query, expected in test_cases:
            decision = FirstLayerDMM(query)
            if decision and any(expected in d for d in decision):
                print(f"✅ '{query}' → {decision[0]}")
            else:
                print(f"⚠️ '{query}' → {decision} (expected {expected})")
                
    except Exception as e:
        print(f"❌ Decision making test failed: {e}")

def test_data_files():
    """Check if data files are in good state"""
    print("\n📁 Testing Data Files...")
    
    data_files = {
        "portfolio.json": "Stock portfolio data",
        "projects.json": "Project management data",
        "dsa_progress.json": "DSA progress tracking",
        "Chatlog.json": "Chat conversation history"
    }
    
    for file, description in data_files.items():
        file_path = f"Data/{file}"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    import json
                    data = json.load(f)
                    print(f"✅ {file}: Valid JSON ({description})")
            except json.JSONDecodeError:
                print(f"⚠️ {file}: Invalid JSON format")
        else:
            print(f"⚠️ {file}: File not found")

if __name__ == "__main__":
    print("🛠️ NEXUS Bug Fix Testing")
    print("=" * 40)
    
    test_stock_fixes()
    test_project_fixes()
    test_font_warnings()
    test_decision_making()
    test_data_files()
    
    print("\n🎉 Bug fix testing complete!")
    print("\n📊 Summary of fixes applied:")
    print("  ✅ Stock rate limiting - Added fallback prices")
    print("  ✅ Font warnings - Suppressed matplotlib warnings")
    print("  ✅ Project deadlines - Fixed past deadline issues")
    print("  ✅ Chart generation - Improved error handling")