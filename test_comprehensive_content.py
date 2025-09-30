# test_comprehensive_content.py

"""
Test the comprehensive DSA content generated from multiple sources
"""

import json

def test_comprehensive_content():
    """Test loading and displaying comprehensive content"""
    print("🧪 TESTING COMPREHENSIVE DSA CONTENT")
    print("=" * 50)
    
    try:
        # Load comprehensive content
        with open('comprehensive_dsa_content_cpp.json', 'r') as f:
            data = json.load(f)
            
        print(f"✅ Loaded comprehensive content successfully!")
        print(f"📚 Total Topics: {data['metadata']['total_topics']}")
        print(f"💻 Language: {data['metadata']['language'].upper()}")
        print(f"🎯 Sources: {len(data['metadata']['sources'])}")
        
        # Display source information
        print("\n📖 SOURCES:")
        for source_key, source_info in data['metadata']['sources'].items():
            print(f"• {source_info['name']}: {source_info['focus']}")
            
        # Test arrays content
        if 'arrays' in data['topics']:
            arrays = data['topics']['arrays']
            print(f"\n🔢 ARRAYS TOPIC SAMPLE:")
            print(f"• Topic: {arrays['topic_name']}")
            print(f"• Difficulty: {arrays['difficulty']}")
            print(f"• Total Problems: {arrays['total_problems']}")
            print(f"• Patterns: {', '.join(arrays['patterns'])}")
            
            # Show Striver content sample
            striver = arrays['striver_content']
            print(f"\n📺 STRIVER CONTENT:")
            print(f"• Problems: {striver['total_problems']}")
            print(f"• YouTube: {striver['youtube_channel']}")
            
            if 'key_concepts' in striver['content']:
                print(f"• Key Concepts: {', '.join(striver['content']['key_concepts'][:3])}...")
                
            # Show C++ implementation sample
            if 'cpp_implementations' in striver['content']:
                cpp_code = striver['content']['cpp_implementations']
                if 'kadanes_algorithm' in cpp_code:
                    print(f"\n💻 C++ IMPLEMENTATION SAMPLE:")
                    code_lines = cpp_code['kadanes_algorithm'].strip().split('\n')[:5]
                    for line in code_lines:
                        print(f"  {line}")
                    print("  ... (full implementation available)")
                    
        print(f"\n🎉 COMPREHENSIVE CONTENT TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading content: {e}")
        return False

def show_all_topics():
    """Show all available topics"""
    try:
        with open('comprehensive_dsa_content_cpp.json', 'r') as f:
            data = json.load(f)
            
        print("\n📚 ALL AVAILABLE TOPICS:")
        print("=" * 40)
        
        for i, (topic_key, topic_data) in enumerate(data['topics'].items(), 1):
            print(f"{i:2d}. {topic_data['topic_name']} ({topic_data['total_problems']} problems)")
            print(f"    Priority: {topic_data['priority']} | Difficulty: {topic_data['difficulty']}")
            print(f"    Patterns: {', '.join(topic_data['patterns'][:2])}{'...' if len(topic_data['patterns']) > 2 else ''}")
            print()
            
    except Exception as e:
        print(f"❌ Error showing topics: {e}")

if __name__ == "__main__":
    if test_comprehensive_content():
        show_all_topics()
    else:
        print("❌ Test failed - comprehensive content not available")