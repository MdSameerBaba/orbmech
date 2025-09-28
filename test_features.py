#!/usr/bin/env python3
"""
Test specific features of NEXUS AI Assistant
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_chatbot():
    """Test the chatbot functionality"""
    print("🤖 Testing Chatbot...")
    try:
        from Backend.Chatbot import ChatBot
        
        test_queries = [
            "Hello, how are you?",
            "What's the weather like?",
            "Tell me a joke",
            "Explain machine learning",
            "What is Python?"
        ]
        
        for query in test_queries:
            print(f"\n🗣️ Query: '{query}'")
            response = ChatBot(query)
            print(f"🤖 Response: {response[:200]}..." if len(response) > 200 else f"🤖 Response: {response}")
            
    except Exception as e:
        print(f"❌ Chatbot test failed: {e}")

def test_realtime_search():
    """Test realtime search functionality"""
    print("\n🌐 Testing Realtime Search...")
    try:
        from Backend.RealtimeSearchEngine import RealtimeSearchEngine
        
        test_queries = [
            "current weather in New York",
            "latest news about AI",
            "Microsoft stock price today"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: '{query}'")
            response = RealtimeSearchEngine(query)
            print(f"🌐 Response: {response[:300]}..." if len(response) > 300 else f"🌐 Response: {response}")
            
    except Exception as e:
        print(f"❌ Realtime search test failed: {e}")

def test_stock_features():
    """Test stock mode features"""
    print("\n📈 Testing Stock Features...")
    try:
        from Backend.Agents.StockAgent import StockAgent, get_stock_price, analyze_portfolio
        
        # Test individual stock price
        symbols = ["AAPL", "MSFT", "GOOGL"]
        for symbol in symbols:
            price = get_stock_price(symbol)
            print(f"💰 {symbol}: ${price:.2f}" if price else f"❌ Could not get {symbol} price")
        
        # Test portfolio analysis
        print("\n📊 Portfolio Analysis:")
        portfolio_analysis = analyze_portfolio()
        print(f"Total Portfolio Value: ${portfolio_analysis['total_portfolio_value']:.2f}")
        print(f"Cash: ${portfolio_analysis['cash']:.2f}")
        print(f"Holdings: {len(portfolio_analysis['holdings_analysis'])}")
        
        # Test stock agent queries
        print("\n🤖 Stock Agent Responses:")
        queries = [
            "What's Apple stock price?",
            "Show my portfolio",
            "How is Microsoft performing?"
        ]
        
        for query in queries:
            print(f"\n🗣️ Query: '{query}'")
            response = StockAgent(query)
            print(f"📈 Response: {response[:300]}..." if len(response) > 300 else f"📈 Response: {response}")
            
    except Exception as e:
        print(f"❌ Stock features test failed: {e}")

def test_dsa_features():
    """Test DSA mode features"""
    print("\n🧠 Testing DSA Features...")
    try:
        from Backend.Agents.DSAAgent import DSAAgent
        
        queries = [
            "arrays guide",
            "show my leetcode progress",
            "trees study guide",
            "dynamic programming prep"
        ]
        
        for query in queries:
            print(f"\n🗣️ Query: '{query}'")
            response = DSAAgent(query)
            print(f"🧠 Response: {response[:400]}..." if len(response) > 400 else f"🧠 Response: {response}")
            
    except Exception as e:
        print(f"❌ DSA features test failed: {e}")

def test_project_features():
    """Test project mode features"""
    print("\n📊 Testing Project Features...")
    try:
        from Backend.Agents.ProjectAgent import ProjectAgent
        
        queries = [
            "show all projects",
            "create project TestApp with Python",
            "project dashboard",
            "git status"
        ]
        
        for query in queries:
            print(f"\n🗣️ Query: '{query}'")
            response = ProjectAgent(query)
            print(f"📊 Response: {response[:400]}..." if len(response) > 400 else f"📊 Response: {response}")
            
    except Exception as e:
        print(f"❌ Project features test failed: {e}")

def test_decision_making():
    """Test the decision making engine"""
    print("\n🧠 Testing Decision Making Engine...")
    try:
        from Backend.Model import FirstLayerDMM
        
        test_queries = [
            "how are you?",
            "open chrome",
            "google search artificial intelligence",
            "what's apple stock price?",
            "arrays guide",
            "create project MyApp",
            "stock mode",
            "tell me a joke"
        ]
        
        for query in test_queries:
            decision = FirstLayerDMM(query)
            print(f"🗣️ '{query}' → 🧠 {decision}")
            
    except Exception as e:
        print(f"❌ Decision making test failed: {e}")

if __name__ == "__main__":
    print("🧪 NEXUS Feature Testing Suite")
    print("="*50)
    
    test_decision_making()
    test_chatbot()
    test_realtime_search()
    test_stock_features()
    test_dsa_features()
    test_project_features()
    
    print("\n✅ Feature testing complete!")