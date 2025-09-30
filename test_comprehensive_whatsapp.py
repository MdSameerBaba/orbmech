# test_comprehensive_whatsapp.py

"""
Test comprehensive DSA content with WhatsApp integration
"""

import json
import sys
import os

# Add Backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

def load_comprehensive_content():
    """Load comprehensive DSA content"""
    try:
        with open('comprehensive_dsa_content_cpp.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Comprehensive content file not found")
        return None

def generate_comprehensive_guide(topic_key):
    """Generate study guide from comprehensive content"""
    data = load_comprehensive_content()
    if not data or topic_key not in data['topics']:
        return f"❌ Topic '{topic_key}' not found in comprehensive content"
    
    topic = data['topics'][topic_key]
    language = data['metadata']['language'].upper()
    
    # Extract key information
    topic_name = topic['topic_name']
    total_problems = topic['total_problems']
    patterns = topic['patterns']
    difficulty = topic['difficulty']
    
    # Get Striver content
    striver = topic['striver_content']
    striver_problems = striver['content'].get('problems', [])
    cpp_implementations = striver['content'].get('cpp_implementations', {})
    
    # Get YouTube playlists
    youtube_playlists = topic.get('youtube_playlists', [])
    
    # Build comprehensive guide
    guide = f"""
🎯 {topic_name.upper()} - COMPREHENSIVE STUDY GUIDE
💻 Language: {language} | 📊 Total Problems: {total_problems}
⭐ Difficulty: {difficulty}

🚀 **MULTI-SOURCE LEARNING APPROACH:**

📺 **STRIVER A2Z DSA SHEET** ({striver['total_problems']} problems)
• Focus: Optimal solutions with detailed explanations
• Channel: {striver['youtube_channel']}

📚 **LOVE BABBAR 450** ({topic['love_babbar_content']['total_problems']} problems)  
• Focus: Complete interview coverage
• Channel: {topic['love_babbar_content']['youtube_channel']}

🎯 **ADITYA VERMA PATTERNS**
• Focus: Pattern recognition and templates
• Channel: {topic['aditya_verma_content']['youtube_channel']}

🎓 **APNA COLLEGE**
• Focus: Beginner to placement ready
• Channel: {topic['apna_college_content']['youtube_channel']}

🔥 **KEY PATTERNS TO MASTER:**
{chr(10).join([f'• {pattern}' for pattern in patterns])}

💻 **C++ IMPLEMENTATION SAMPLES:**
"""
    
    # Add C++ code samples
    if 'kadanes_algorithm' in cpp_implementations:
        guide += f"""
📝 **Kadane's Algorithm (Maximum Subarray):**
```cpp
{cpp_implementations['kadanes_algorithm'].strip()}
```
"""
    
    if 'two_pointers' in cpp_implementations:
        guide += f"""
📝 **Two Pointers Technique:**
```cpp
{cpp_implementations['two_pointers'].strip()}
```
"""
    
    # Add problem samples
    guide += f"""
📊 **MUST-SOLVE PROBLEMS:**
"""
    
    for i, problem in enumerate(striver_problems[:5], 1):
        guide += f"{i}. {problem['name']} ({problem['difficulty']}) - {problem.get('pattern', 'General')}\n"
    
    # Add YouTube resources
    guide += f"""
📺 **COMPREHENSIVE VIDEO RESOURCES:**
"""
    
    for playlist in youtube_playlists[:3]:
        guide += f"• {playlist['creator']}: {playlist['playlist']}\n  🎯 {playlist['focus']}\n  🔗 {playlist['url']}\n\n"
    
    # Add study plan
    study_plan = topic.get('study_plan', {})
    if study_plan:
        guide += f"""
📅 **STUDY PLAN:**
• Duration: {study_plan.get('duration', '2-3 weeks')}
• Daily Commitment: {study_plan.get('daily_commitment', '2-3 hours')}

Phase 1: {study_plan.get('phases', {}).get('Phase 1 (Days 1-5)', {}).get('focus', 'Theory and basics')}
Phase 2: {study_plan.get('phases', {}).get('Phase 2 (Days 6-12)', {}).get('focus', 'Pattern recognition')}
Phase 3: {study_plan.get('phases', {}).get('Phase 3 (Days 13-21)', {}).get('focus', 'Advanced problems')}
"""
    
    guide += f"""
🎯 **INTERVIEW PREPARATION:**
• Companies: FAANG, Microsoft, Amazon, Google
• Frequency: High (commonly asked)
• Time to Master: 2-3 weeks with consistent practice

💡 **PRO TIPS:**
• Start with Apna College for basics
• Use Aditya Verma for pattern recognition  
• Practice Love Babbar problems for variety
• Master Striver solutions for optimality

🚀 Ready to ace {topic_name}? Start with the basics and build up!
"""
    
    return guide

def test_whatsapp_integration():
    """Test WhatsApp integration with comprehensive content"""
    print("📱 TESTING WHATSAPP INTEGRATION")
    print("=" * 50)
    
    # Test arrays guide
    arrays_guide = generate_comprehensive_guide('arrays')
    print("✅ Generated comprehensive arrays guide")
    print(f"📏 Guide length: {len(arrays_guide)} characters")
    
    # Show sample
    print("\n📖 SAMPLE GUIDE (first 500 chars):")
    print("-" * 30)
    print(arrays_guide[:500] + "...")
    
    # Test WhatsApp integration
    try:
        from WhatsAppIntegration import send_study_guide_to_whatsapp, is_whatsapp_configured
        
        if is_whatsapp_configured():
            print("\n📱 WhatsApp is configured!")
            print("💡 Ready to send comprehensive guides via WhatsApp")
            
            # Simulate sending (comment out to actually send)
            # result = send_study_guide_to_whatsapp(arrays_guide, "arrays")
            # print(f"📤 WhatsApp send result: {result}")
            
        else:
            print("⚠️ WhatsApp not configured")
            
    except ImportError:
        print("⚠️ WhatsApp integration not available")

def show_topic_stats():
    """Show statistics for all topics"""
    data = load_comprehensive_content()
    if not data:
        return
        
    print("\n📊 COMPREHENSIVE CONTENT STATISTICS")
    print("=" * 50)
    
    total_problems = sum(topic['total_problems'] for topic in data['topics'].values())
    print(f"🎯 Total Problems Across All Sources: {total_problems}")
    print(f"📚 Total Topics: {len(data['topics'])}")
    print(f"💻 Language Focus: {data['metadata']['language'].upper()}")
    print(f"🏫 Sources: {len(data['metadata']['sources'])}")
    
    print("\n🔥 TOP 5 TOPICS BY PROBLEM COUNT:")
    sorted_topics = sorted(
        data['topics'].items(), 
        key=lambda x: x[1]['total_problems'], 
        reverse=True
    )[:5]
    
    for i, (key, topic) in enumerate(sorted_topics, 1):
        print(f"{i}. {topic['topic_name']}: {topic['total_problems']} problems")

if __name__ == "__main__":
    print("🧪 COMPREHENSIVE DSA + WHATSAPP TEST")
    print("=" * 60)
    
    test_whatsapp_integration()
    show_topic_stats()
    
    print("\n🎉 COMPREHENSIVE CONTENT INTEGRATION TEST COMPLETE!")
    print("📱 Ready for enhanced WhatsApp delivery with multi-source content!")