# comprehensive_dsa_whatsapp.py

"""
🚀 COMPREHENSIVE DSA WHATSAPP INTEGRATION
=========================================

Combines content from:
- Striver A2Z DSA Sheet (TakeUForward) 
- Love Babbar DSA Sheet & YouTube
- Aditya Verma DSA Patterns
- Apna College DSA Series

Language: C++ focused
WhatsApp: Direct delivery with 5-minute scheduling
"""

import json
import sys
import os

# Add Backend path for WhatsApp integration
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backend'))

try:
    from WhatsAppIntegration import (
        send_study_guide_to_whatsapp,
        send_dsa_progress_to_whatsapp,
        is_whatsapp_configured
    )
    WHATSAPP_ENABLED = True
    print("✅ WhatsApp integration loaded successfully!")
except ImportError as e:
    print(f"⚠️ WhatsApp integration not available: {e}")
    WHATSAPP_ENABLED = False

def load_comprehensive_content():
    """Load comprehensive DSA content"""
    try:
        with open('comprehensive_dsa_content_cpp.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Comprehensive content file not found")
        return None

def get_topic_mapping():
    """Get topic mapping for user queries"""
    return {
        'arrays': ['array', 'arrays', 'vector', 'vectors'],
        'strings': ['string', 'strings', 'text', 'pattern'],
        'linked_lists': ['linked', 'list', 'lists', 'node'],
        'binary_trees': ['tree', 'trees', 'binary tree', 'bst'],
        'binary_search_trees': ['bst', 'binary search tree'],
        'binary_search': ['binary search', 'search', 'bs'],
        'stacks_queues': ['stack', 'queue', 'stacks', 'queues'],
        'heaps': ['heap', 'heaps', 'priority queue'],
        'hashing': ['hash', 'hashing', 'hashmap', 'map'],
        'recursion': ['recursion', 'recursive', 'backtrack'],
        'dynamic_programming': ['dp', 'dynamic', 'programming', 'memoization'],
        'graphs': ['graph', 'graphs', 'dfs', 'bfs'],
        'tries': ['trie', 'tries', 'prefix tree'],
        'greedy': ['greedy', 'greedy algorithms'],
        'bit_manipulation': ['bit', 'bits', 'bitwise', 'manipulation']
    }

def find_topic_from_query(query):
    """Find topic from user query"""
    query_lower = query.lower()
    topic_mapping = get_topic_mapping()
    
    for topic_key, keywords in topic_mapping.items():
        for keyword in keywords:
            if keyword in query_lower:
                return topic_key
    
    return 'arrays'  # Default fallback

def generate_comprehensive_guide(topic_key):
    """Generate comprehensive study guide with all sources"""
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
    
    # Get source-specific content
    striver = topic['striver_content']
    love_babbar = topic['love_babbar_content']
    aditya_verma = topic['aditya_verma_content']
    apna_college = topic['apna_college_content']
    
    # Get implementations
    striver_problems = striver['content'].get('problems', [])
    cpp_implementations = striver['content'].get('cpp_implementations', {})
    
    # Build comprehensive guide
    guide = f"""🎯 {topic_name.upper()} - COMPREHENSIVE STUDY GUIDE
💻 Language: {language} | 📊 Total Problems: {total_problems}
⭐ Difficulty: {difficulty}

🚀 **MULTI-SOURCE LEARNING ROADMAP:**

📺 **STRIVER A2Z DSA SHEET** ({striver['total_problems']} problems)
• Approach: {striver['approach']}
• Channel: Take U Forward
• Focus: Optimal solutions with detailed complexity analysis

📚 **LOVE BABBAR 450 DSA** ({love_babbar['total_problems']} problems)
• Approach: {love_babbar['approach']}
• Channel: CodeHelp by Love Babbar
• Focus: Complete interview preparation coverage

🎯 **ADITYA VERMA PATTERNS**
• Approach: {aditya_verma['approach']}
• Channel: Aditya Verma Programming
• Focus: Template-based pattern recognition

🎓 **APNA COLLEGE DSA**
• Approach: {apna_college['approach']}
• Channel: Apna College Official
• Focus: Beginner to placement preparation

🔥 **MUST-MASTER PATTERNS:**
{chr(10).join([f'• {pattern}' for pattern in patterns])}

💻 **C++ IMPLEMENTATION TEMPLATES:**
"""
    
    # Add C++ code samples with better formatting
    if 'kadanes_algorithm' in cpp_implementations:
        guide += f"""
📝 **Kadane's Algorithm - Maximum Subarray Sum:**
```cpp
{cpp_implementations['kadanes_algorithm'].strip()}
```

🎯 **Time Complexity:** O(n) | **Space Complexity:** O(1)
💡 **Pattern:** Dynamic Programming on Arrays
"""
    
    if 'two_pointers' in cpp_implementations:
        guide += f"""
📝 **Two Pointers Technique - Two Sum:**
```cpp
{cpp_implementations['two_pointers'].strip()}
```

🎯 **Time Complexity:** O(n) | **Space Complexity:** O(1)  
💡 **Pattern:** Two Pointers on Sorted Array
"""
    
    # Add top problems to solve
    guide += f"""
🏆 **TOP PROBLEMS TO MASTER:**"""
    
    for i, problem in enumerate(striver_problems[:8], 1):
        guide += f"""
{i}. **{problem['name']}** ({problem['difficulty']})
   🎯 Pattern: {problem.get('pattern', 'General')}
   💡 Companies: Google, Meta, Amazon, Microsoft"""
    
    # Add study plan
    study_plan = topic.get('study_plan', {})
    if study_plan:
        guide += f"""

📅 **3-WEEK STUDY PLAN:**
• **Duration:** {study_plan.get('duration', '2-3 weeks')}
• **Daily Time:** {study_plan.get('daily_commitment', '2-3 hours')}

**Week 1:** {study_plan.get('phases', {}).get('Phase 1 (Days 1-5)', {}).get('focus', 'Theory and basics')}
**Week 2:** {study_plan.get('phases', {}).get('Phase 2 (Days 6-12)', {}).get('focus', 'Pattern recognition')}  
**Week 3:** {study_plan.get('phases', {}).get('Phase 3 (Days 13-21)', {}).get('focus', 'Advanced optimization')}"""
    
    # Add YouTube playlists
    youtube_playlists = topic.get('youtube_playlists', [])
    if youtube_playlists:
        guide += f"""

📺 **COMPLETE VIDEO PLAYLISTS:**"""
        
        for playlist in youtube_playlists:
            guide += f"""
• **{playlist['creator']}:** {playlist['playlist']}
  🎯 {playlist['focus']}
  🔗 {playlist['url']}"""
    
    # Add interview preparation
    guide += f"""

🎯 **INTERVIEW PREPARATION:**
• **Companies:** FAANG, Microsoft, Amazon, Google, Netflix
• **Frequency:** Very High (asked in 80%+ technical interviews)
• **Preparation Time:** 2-3 weeks with consistent practice
• **Success Rate:** 95% with proper pattern mastery

💡 **LEARNING PATH RECOMMENDATION:**
1. **Start:** Apna College (basics & intuition)
2. **Develop:** Aditya Verma (pattern recognition)
3. **Practice:** Love Babbar (variety & coverage)
4. **Master:** Striver (optimal solutions)

🚀 **Ready to dominate {topic_name}? Start with theory, master patterns, then optimize!**

📱 **Need help?** Reply with:
• "send progress to whatsapp" - Get your coding progress
• "send [topic] guide to whatsapp" - Get another topic guide  
• "help" - Get more commands

💪 You've got this! Master one topic at a time! 🔥"""
    
    return guide

def handle_dsa_command(query):
    """Handle DSA commands with comprehensive content"""
    query_lower = query.lower()
    
    # Check for WhatsApp guide requests
    if any(word in query_lower for word in ['guide', 'study']) and 'whatsapp' in query_lower:
        topic = find_topic_from_query(query)
        
        print(f"📱 Preparing {topic} study guide for WhatsApp...")
        guide = generate_comprehensive_guide(topic)
        
        if WHATSAPP_ENABLED and is_whatsapp_configured():
            try:
                result = send_study_guide_to_whatsapp(guide, topic)
                return f"""📱 **COMPREHENSIVE {topic.upper()} GUIDE SENT!**

✅ WhatsApp delivery scheduled successfully!
📚 Source: Striver + Love Babbar + Aditya Verma + Apna College
💻 Language: C++ focused implementations
📊 Content: Complete interview preparation guide

🕐 Check your WhatsApp in ~5 minutes for the full guide!

{result}"""
            except Exception as e:
                return f"❌ WhatsApp delivery failed: {e}\n\n{guide}"
        else:
            return f"⚠️ WhatsApp not configured\n\n{guide}"
    
    # Check for progress requests  
    elif 'progress' in query_lower and 'whatsapp' in query_lower:
        if WHATSAPP_ENABLED and is_whatsapp_configured():
            try:
                result = send_dsa_progress_to_whatsapp()
                return f"""📊 **DSA PROGRESS SENT TO WHATSAPP!**

✅ Progress report scheduled successfully!
📈 Includes: LeetCode + CodeChef statistics
🎯 Platform: Multi-platform tracking

🕐 Check your WhatsApp in ~5 minutes!

{result}"""
            except Exception as e:
                return f"❌ Progress delivery failed: {e}"
        else:
            return "⚠️ WhatsApp not configured for progress reports"
    
    # Just guide request (no WhatsApp)
    elif any(word in query_lower for word in ['guide', 'study']):
        topic = find_topic_from_query(query)
        return generate_comprehensive_guide(topic)
    
    # Default help
    else:
        return """🚀 **COMPREHENSIVE DSA SYSTEM**

📱 **WhatsApp Commands:**
• "send arrays guide to whatsapp"
• "send dp guide to whatsapp"  
• "send progress to whatsapp"

📚 **Available Topics:**
Arrays, Strings, Linked Lists, Trees, BST, Binary Search,
Stacks/Queues, Heaps, Hashing, Recursion, DP, Graphs,
Tries, Greedy, Bit Manipulation

💻 **Language Focus:** C++
🎯 **Sources:** Striver + Love Babbar + Aditya Verma + Apna College

Try: "send trees guide to whatsapp" for comprehensive content!"""

def test_comprehensive_system():
    """Test the comprehensive DSA system"""
    print("🧪 TESTING COMPREHENSIVE DSA SYSTEM")
    print("=" * 50)
    
    # Test commands
    test_commands = [
        "send arrays guide to whatsapp",
        "send dp guide to whatsapp", 
        "send progress to whatsapp",
        "trees guide",
        "help"
    ]
    
    for cmd in test_commands:
        print(f"\n🔍 Testing: '{cmd}'")
        print("-" * 30)
        result = handle_dsa_command(cmd)
        print(result[:200] + "..." if len(result) > 200 else result)

if __name__ == "__main__":
    # Test the system
    test_comprehensive_system()
    
    print("\n🎉 COMPREHENSIVE DSA WHATSAPP SYSTEM READY!")
    print("📱 Enhanced with multi-source content")
    print("💻 C++ focused implementations")
    print("🚀 Ready for WhatsApp delivery!")