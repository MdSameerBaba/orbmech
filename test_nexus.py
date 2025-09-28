#!/usr/bin/env python3
"""
NEXUS AI Assistant - Comprehensive Testing Suite
Testing all features and identifying bugs for debugging
"""

import os
import sys
import json
import importlib.util
import traceback
from datetime import datetime
import subprocess

# Add the project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class NEXUSTestSuite:
    def __init__(self):
        self.test_results = {
            "environment": [],
            "core_system": [],
            "general_mode": [],
            "stock_mode": [],
            "dsa_mode": [],
            "project_mode": [],
            "voice_tts": [],
            "gui": []
        }
        self.errors_found = []
        self.warnings = []
        
    def log_result(self, category, test_name, status, message="", error=None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,  # PASS, FAIL, WARNING
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if error:
            result["error"] = str(error)
            result["traceback"] = traceback.format_exc()
            
        self.test_results[category].append(result)
        
        if status == "FAIL":
            self.errors_found.append(f"{category}: {test_name} - {message}")
        elif status == "WARNING":
            self.warnings.append(f"{category}: {test_name} - {message}")
            
    def test_environment(self):
        """Test environment setup and dependencies"""
        print("🔧 Testing Environment Setup...")
        
        # Test .env file
        try:
            from dotenv import dotenv_values
            env_vars = dotenv_values(".env")
            
            required_vars = ["Username", "Assistantname", "GroqAPIKey"]
            missing_vars = [var for var in required_vars if not env_vars.get(var)]
            
            if missing_vars:
                self.log_result("environment", ".env Configuration", "FAIL", 
                              f"Missing required variables: {missing_vars}")
            else:
                self.log_result("environment", ".env Configuration", "PASS", 
                              "All required environment variables present")
        except Exception as e:
            self.log_result("environment", ".env Configuration", "FAIL", 
                          "Failed to load environment variables", e)
        
        # Test critical imports
        critical_modules = [
            ("groq", "Groq API client"),
            ("pygame", "Audio system"),
            ("PyQt5", "GUI framework"),
            ("yfinance", "Stock data"),
            ("requests", "HTTP requests"),
            ("bs4", "Web scraping")
        ]
        
        for module, description in critical_modules:
            try:
                __import__(module)
                self.log_result("environment", f"Import {module}", "PASS", 
                              f"{description} available")
            except ImportError as e:
                self.log_result("environment", f"Import {module}", "FAIL", 
                              f"{description} not available", e)
    
    def test_core_system(self):
        """Test core system components"""
        print("🚀 Testing Core System...")
        
        # Test Model.py (Decision Making)
        try:
            from Backend.Model import FirstLayerDMM, client
            if client is None:
                self.log_result("core_system", "Groq Client", "FAIL", 
                              "Groq client not initialized")
            else:
                # Test decision making
                test_query = "how are you today?"
                decision = FirstLayerDMM(test_query)
                if isinstance(decision, list) and len(decision) > 0:
                    self.log_result("core_system", "Decision Making", "PASS", 
                                  f"Query classified as: {decision}")
                else:
                    self.log_result("core_system", "Decision Making", "WARNING", 
                                  f"Unexpected decision format: {decision}")
        except Exception as e:
            self.log_result("core_system", "Decision Making", "FAIL", 
                          "FirstLayerDMM failed", e)
        
        # Test ModeManager
        try:
            from Backend.ModeManager import get_current_mode, load_system_mode
            current_mode = get_current_mode()
            self.log_result("core_system", "Mode Manager", "PASS", 
                          f"Current mode: {current_mode}")
        except Exception as e:
            self.log_result("core_system", "Mode Manager", "FAIL", 
                          "Mode management failed", e)
        
        # Test SharedServices
        try:
            from Backend.SharedServices import gui_queue, backend_queue
            self.log_result("core_system", "Shared Services", "PASS", 
                          "Communication queues initialized")
        except Exception as e:
            self.log_result("core_system", "Shared Services", "FAIL", 
                          "Queue communication failed", e)
    
    def test_general_mode(self):
        """Test General Mode features"""
        print("🤖 Testing General Mode...")
        
        # Test Chatbot
        try:
            from Backend.Chatbot import ChatBot
            response = ChatBot("Hello, this is a test")
            if response and len(response) > 0:
                self.log_result("general_mode", "Chatbot", "PASS", 
                              f"Response length: {len(response)} chars")
            else:
                self.log_result("general_mode", "Chatbot", "WARNING", 
                              "Empty or no response from chatbot")
        except Exception as e:
            self.log_result("general_mode", "Chatbot", "FAIL", 
                          "Chatbot failed", e)
        
        # Test Automation
        try:
            from Backend.Automation import Automation
            # Don't actually run automation, just test import
            self.log_result("general_mode", "Automation", "PASS", 
                          "Automation module loaded")
        except Exception as e:
            self.log_result("general_mode", "Automation", "FAIL", 
                          "Automation module failed", e)
        
        # Test RealtimeSearchEngine
        try:
            from Backend.RealtimeSearchEngine import RealtimeSearchEngine
            # Test with a simple query
            result = RealtimeSearchEngine("current weather")
            if result:
                self.log_result("general_mode", "Realtime Search", "PASS", 
                              "Search engine responding")
            else:
                self.log_result("general_mode", "Realtime Search", "WARNING", 
                              "No response from search engine")
        except Exception as e:
            self.log_result("general_mode", "Realtime Search", "FAIL", 
                          "Search engine failed", e)
        
        # Test FileReader
        try:
            from Backend.FileReader import get_text_from_pdf, summarize_text
            self.log_result("general_mode", "File Reader", "PASS", 
                          "PDF processing module loaded")
        except Exception as e:
            self.log_result("general_mode", "File Reader", "FAIL", 
                          "PDF processing failed", e)
    
    def test_stock_mode(self):
        """Test Stock Mode features"""
        print("📈 Testing Stock Mode...")
        
        try:
            from Backend.Agents.StockAgent import StockAgent, get_stock_price, load_portfolio
            
            # Test stock price fetching
            test_symbol = "AAPL"
            price = get_stock_price(test_symbol)
            if price and price > 0:
                self.log_result("stock_mode", "Stock Price Fetch", "PASS", 
                              f"{test_symbol} price: ${price:.2f}")
            else:
                self.log_result("stock_mode", "Stock Price Fetch", "WARNING", 
                              f"Could not fetch {test_symbol} price")
            
            # Test portfolio loading
            portfolio = load_portfolio()
            if isinstance(portfolio, dict):
                self.log_result("stock_mode", "Portfolio Loading", "PASS", 
                              f"Portfolio loaded with {len(portfolio.get('holdings', {}))} holdings")
            else:
                self.log_result("stock_mode", "Portfolio Loading", "FAIL", 
                              "Portfolio format invalid")
            
            # Test StockAgent
            response = StockAgent("What is Apple stock price?")
            if response and len(response) > 0:
                self.log_result("stock_mode", "Stock Agent", "PASS", 
                              "Stock agent responding")
            else:
                self.log_result("stock_mode", "Stock Agent", "WARNING", 
                              "Stock agent not responding")
                
        except Exception as e:
            self.log_result("stock_mode", "Stock Mode", "FAIL", 
                          "Stock mode failed", e)
    
    def test_dsa_mode(self):
        """Test DSA Mode features"""
        print("🧠 Testing DSA Mode...")
        
        try:
            from Backend.Agents.DSAAgent import DSAAgent
            
            # Test DSA Agent
            response = DSAAgent("arrays guide")
            if response and len(response) > 0:
                self.log_result("dsa_mode", "DSA Agent", "PASS", 
                              "DSA agent responding")
            else:
                self.log_result("dsa_mode", "DSA Agent", "WARNING", 
                              "DSA agent not responding")
                
        except Exception as e:
            self.log_result("dsa_mode", "DSA Mode", "FAIL", 
                          "DSA mode failed", e)
        
        # Check if DSA data files exist
        dsa_files = ["dsa_progress.json", "dsa_study_guides.json"]
        for file in dsa_files:
            file_path = f"Data/{file}"
            if os.path.exists(file_path):
                self.log_result("dsa_mode", f"DSA Data File ({file})", "PASS", 
                              "Data file exists")
            else:
                self.log_result("dsa_mode", f"DSA Data File ({file})", "WARNING", 
                              "Data file missing - will be created on first use")
    
    def test_project_mode(self):
        """Test Project Mode features"""
        print("📊 Testing Project Mode...")
        
        try:
            from Backend.Agents.ProjectAgent import ProjectAgent
            
            # Test ProjectAgent
            response = ProjectAgent("show all projects")
            if response and len(response) > 0:
                self.log_result("project_mode", "Project Agent", "PASS", 
                              "Project agent responding")
            else:
                self.log_result("project_mode", "Project Agent", "WARNING", 
                              "Project agent not responding")
                
        except Exception as e:
            self.log_result("project_mode", "Project Mode", "FAIL", 
                          "Project mode failed", e)
        
        # Test Git availability
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log_result("project_mode", "Git Integration", "PASS", 
                              f"Git available: {result.stdout.strip()}")
            else:
                self.log_result("project_mode", "Git Integration", "WARNING", 
                              "Git not available or not in PATH")
        except Exception as e:
            self.log_result("project_mode", "Git Integration", "WARNING", 
                          "Could not check Git availability", e)
    
    def test_voice_tts(self):
        """Test Voice and TTS functionality"""
        print("🔊 Testing Voice & TTS...")
        
        # Test Text-to-Speech
        try:
            from Backend.TextToSpeech import TextToSpeech
            # Don't actually speak, just test import
            self.log_result("voice_tts", "Text-to-Speech", "PASS", 
                          "TTS module loaded")
        except Exception as e:
            self.log_result("voice_tts", "Text-to-Speech", "FAIL", 
                          "TTS module failed", e)
        
        # Test Speech-to-Text
        try:
            from Backend.SpeechToText import prepare_speech_engine
            # Don't actually listen, just test import
            self.log_result("voice_tts", "Speech-to-Text", "PASS", 
                          "STT module loaded")
        except Exception as e:
            self.log_result("voice_tts", "Speech-to-Text", "FAIL", 
                          "STT module failed", e)
        
        # Test Pygame audio
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.quit()
            self.log_result("voice_tts", "Audio System", "PASS", 
                          "Pygame audio system working")
        except Exception as e:
            self.log_result("voice_tts", "Audio System", "FAIL", 
                          "Pygame audio failed", e)
    
    def test_gui(self):
        """Test GUI components (without actually launching)"""
        print("🖥️ Testing GUI Components...")
        
        try:
            from Interface.GUI import GraphicalUserInterface
            self.log_result("gui", "GUI Import", "PASS", 
                          "GUI module loaded successfully")
        except Exception as e:
            self.log_result("gui", "GUI Import", "FAIL", 
                          "GUI module failed to load", e)
        
        # Check if required GUI files exist
        gui_files = [
            "Interface/Graphics/activate.wav",
            "Interface/Graphics",
            "Interface/Files"
        ]
        
        for file_path in gui_files:
            if os.path.exists(file_path):
                self.log_result("gui", f"GUI Resource ({os.path.basename(file_path)})", "PASS", 
                              "Resource exists")
            else:
                self.log_result("gui", f"GUI Resource ({os.path.basename(file_path)})", "WARNING", 
                              "Resource missing")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting NEXUS AI Assistant Test Suite...")
        print("=" * 60)
        
        self.test_environment()
        self.test_core_system()
        self.test_general_mode()
        self.test_stock_mode()
        self.test_dsa_mode()
        self.test_project_mode()
        self.test_voice_tts()
        self.test_gui()
        
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        warning_tests = 0
        
        for category, tests in self.test_results.items():
            if tests:
                print(f"\n🔹 {category.upper().replace('_', ' ')}:")
                for test in tests:
                    status_emoji = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}
                    emoji = status_emoji.get(test["status"], "❓")
                    print(f"  {emoji} {test['test']}: {test['message']}")
                    
                    total_tests += 1
                    if test["status"] == "PASS":
                        passed_tests += 1
                    elif test["status"] == "FAIL":
                        failed_tests += 1
                    elif test["status"] == "WARNING":
                        warning_tests += 1
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"  Total Tests: {total_tests}")
        print(f"  ✅ Passed: {passed_tests}")
        print(f"  ❌ Failed: {failed_tests}")
        print(f"  ⚠️ Warnings: {warning_tests}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"  🎯 Success Rate: {success_rate:.1f}%")
        
        if self.errors_found:
            print(f"\n🚨 CRITICAL ISSUES FOUND ({len(self.errors_found)}):")
            for i, error in enumerate(self.errors_found, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️ WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        # Save detailed report to file
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": warning_tests,
                "success_rate": success_rate
            },
            "detailed_results": self.test_results,
            "errors": self.errors_found,
            "warnings": self.warnings
        }
        
        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: test_report.json")
        print("=" * 60)

if __name__ == "__main__":
    tester = NEXUSTestSuite()
    tester.run_all_tests()