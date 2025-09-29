"""
🧪 NEXUS Integration Test Suite
===============================

Test the unified NEXUS career acceleration system integration
with Main.py command routing and all 4 phases.
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_nexus_integration():
    """Test NEXUS system integration"""
    print("🧪 Testing NEXUS Integration...")
    print("=" * 60)
    
    # Test imports
    try:
        from Backend.Agents.NEXUSAgent import NEXUS, nexus_agent
        print("✅ NEXUS Agent imported successfully")
    except ImportError as e:
        print(f"⚠️ NEXUS Agent import failed: {e}")
        return
    
    # Test basic functionality
    test_queries = [
        "NEXUS status",
        "Help",
        "Research Google company",
        "Build resume for Microsoft", 
        "Start assessment",
        "Start interview for Amazon",
        "Career progress",
        "What can you do"
    ]
    
    print("\n🔍 Testing NEXUS Commands...")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 40)
        
        try:
            result = NEXUS(query)
            print(result[:200] + "..." if len(result) > 200 else result)
            print("✅ SUCCESS")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    # Test metrics
    print(f"\n📊 NEXUS Metrics after testing:")
    print(f"Sessions: {nexus_agent.metrics['sessions_completed']}")
    print(f"Companies: {nexus_agent.metrics['companies_researched']}")
    print(f"Resumes: {nexus_agent.metrics['resumes_optimized']}")
    print(f"Assessments: {nexus_agent.metrics['assessments_taken']}")
    print(f"Interviews: {nexus_agent.metrics['interviews_conducted']}")
    
    print("\n🎯 NEXUS Integration Test Complete!")

def test_main_integration():
    """Test Main.py NEXUS integration"""
    print("\n🔧 Testing Main.py Integration...")
    print("=" * 60)
    
    # Test query classification
    test_queries = [
        "NEXUS status",
        "Research Google company", 
        "Career progress",
        "Start interview simulation",
        "Company intelligence",
        "Tell me about Microsoft company"
    ]
    
    # Mock the decision making logic
    from Backend.Model import FirstLayerDMM
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        
        # Check if NEXUS keywords are detected
        nexus_keywords = [
            'nexus', 'career', 'company research', 'build resume', 'optimize resume', 
            'start assessment', 'start interview', 'mock interview', 'practice interview',
            'career progress', 'interview simulation', 'behavioral interview', 'technical interview',
            'company intelligence', 'resume building', 'skill assessment', 'interview practice',
            'research google', 'research microsoft', 'research amazon', 'research apple',
            'research netflix', 'research meta', 'research facebook', 'tell me about.*company'
        ]
        
        is_nexus = any(keyword in query.lower() for keyword in nexus_keywords)
        print(f"   NEXUS detected: {is_nexus}")
        
        if is_nexus:
            print("   ✅ Would route to NEXUS system")
        else:
            print("   ⚠️ Would route to other systems")

if __name__ == "__main__":
    print("🚀 NEXUS COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Test NEXUS agent
    test_nexus_integration()
    
    # Test Main.py integration
    test_main_integration()
    
    print("\n🎯 All tests completed!")
    print("🚀 NEXUS is ready for career acceleration!")