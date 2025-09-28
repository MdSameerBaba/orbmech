#!/usr/bin/env python3
"""
Test the fixed project switching logic
"""

import sys
sys.path.append('.')
sys.path.append('Backend')

from Backend.Model import FirstLayerDMM

def test_decision_making():
    """Test how the decision making processes project switch commands"""
    
    print("🧪 Testing Decision Making for Project Switch...\n")
    
    # Test the problematic command
    query = "switch to NEXUS Test Project"
    print(f"Query: '{query}'")
    
    decision = FirstLayerDMM(query)
    print(f"Decision: {decision}")
    
    # Test other variations
    test_queries = [
        "switch to TestRepo",
        "switch to project TestRepo", 
        "current project",
        "git status"
    ]
    
    for test_query in test_queries:
        print(f"\nQuery: '{test_query}'")
        decision = FirstLayerDMM(test_query)
        print(f"Decision: {decision}")

if __name__ == "__main__":
    test_decision_making()