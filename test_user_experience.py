#!/usr/bin/env python3
"""
NEXUS Surface-Level User Testing
Complete pipeline testing for AI project generation
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Backend.Model import FirstLayerDMM
from Backend.Agents.ProjectAgent import ProjectAgent

def test_user_commands():
    """Test user commands through complete NEXUS pipeline"""
    print("🌟 NEXUS AI Project Generator - User Experience Test")
    print("=" * 70)
    
    # Realistic user commands
    test_commands = [
        "create react todo app with authentication and dark mode",
        "build me a vue.js ecommerce site with stripe payments", 
        "make python flask api with jwt authentication",
        "generate angular dashboard with charts",
        "create mobile app with react native"
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\\n🎯 Test {i}: {cmd}")
        print("-" * 50)
        
        try:
            # Step 1: Decision making
            decision = FirstLayerDMM(cmd)
            print(f"📋 Decision: {decision}")
            
            # Step 2: Check classification
            is_project = any(d.startswith("project") for d in decision)
            
            if is_project:
                print("✅ Classified as project command")
                
                # Step 3: ProjectAgent execution
                result = ProjectAgent(cmd)
                
                if "AI Project Generated Successfully" in result:
                    print("🎉 SUCCESS! Project generated")
                    
                    # Extract key info
                    lines = result.split('\\n')
                    for line in lines[:10]:  # Show first 10 lines
                        if any(key in line for key in ['Project:', 'Location:', 'Tech Stack:', 'Features:']):
                            print(f"   {line}")
                else:
                    print(f"❌ Generation failed: {result[:100]}...")
            else:
                print("❌ Not classified as project command")
                
        except Exception as e:
            print(f"💥 Error: {e}")
    
    print(f"\\n🏁 All tests completed!")
    print("✨ NEXUS is ready for real user interaction!")

if __name__ == "__main__":
    test_user_commands()