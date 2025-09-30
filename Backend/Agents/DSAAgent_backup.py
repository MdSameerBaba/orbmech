# In Backend/Agents/DSAAgent.py

import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dotenv import dotenv_values
from groq import Groq
import requests
from bs4 import BeautifulSoup
import warnings
import sys
import os

# Add Backend path for WhatsApp integration
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from WhatsAppIntegration import (
        send_dsa_progress_to_whatsapp, 
        send_study_guide_to_whatsapp,
        send_scraped_content_to_whatsapp,
        is_whatsapp_configured
    )
    WHATSAPP_ENABLED = True
    print("✅ WhatsApp integration loaded successfully!")
except ImportError as e:
    print(f"⚠️ WhatsApp integration not available: {e}")
    WHATSAPP_ENABLED = False

# Suppress matplotlib font warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*missing from font.*")
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in DSAAgent: {e}")
    client = None

DSA_FILE = r"Data\dsa_progress.json"

# --- HELPER FUNCTIONS ---
def load_dsa_progress():
    try:
        with open(DSA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"topics": {}, "platform_data": {}}

def save_dsa_progress(data):
    try:
        with open(DSA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving DSA progress: {e}")

def load_study_guides():
    """Load comprehensive study guides from JSON file"""
    try:
        # First try to load comprehensive content
        with open('comprehensive_dsa_content_cpp.json', 'r') as file:
            comprehensive_data = json.load(file)
            return convert_comprehensive_to_guide_format(comprehensive_data)
    except FileNotFoundError:
        try:
            # Fallback to enhanced content
            with open('enhanced_dsa_content.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # Final fallback to basic content
            return {
                "programming_language": "C++",
                "guides": {
                    "arrays": {
                        "title": "Arrays & Strings",
                        "youtube_videos": [
                            {"title": "Array Basics", "channel": "TechChannel", "url": "https://youtube.com/watch?v=example1"},
                        ],
                        "leetcode_problems": [
                            {"name": "Two Sum", "difficulty": "Easy", "url": "https://leetcode.com/problems/two-sum/"},
                        ],
                        "codechef_problems": [
                            {"name": "Array Sum", "difficulty": "Easy", "url": "https://codechef.com/problems/ARRAYSUM"},
                        ]
                    }
                }
            }

def convert_comprehensive_to_guide_format(comprehensive_data):
    """Convert comprehensive DSA content to guide format"""
    guides = {}
    language = comprehensive_data["metadata"]["language"]
    
    for topic_key, topic_data in comprehensive_data["topics"].items():
        # Extract YouTube playlists
        youtube_videos = []
        for playlist in topic_data.get("youtube_playlists", []):
            youtube_videos.append({
                "title": playlist["playlist"],
                "channel": playlist["creator"],
                "url": playlist["url"],
                "duration": "Multiple videos",
                "difficulty": "All levels",
                "topics_covered": topic_data.get("patterns", []),
                "focus": playlist["focus"]
            })
        
        # Extract practice problems from Striver content
        leetcode_problems = []
        striver_problems = topic_data.get("striver_content", {}).get("content", {}).get("problems", [])
        for i, problem in enumerate(striver_problems[:10]):  # Limit to 10 for display
            leetcode_problems.append({
                "name": problem["name"],
                "difficulty": problem["difficulty"],
                "url": f"https://leetcode.com/problems/{problem['name'].lower().replace(' ', '-')}/",
                "pattern": problem.get("pattern", "General")
            })
        
        # Create CodeChef problems based on topic
        codechef_problems = [
            {
                "name": f"{topic_data['topic_name']} Practice",
                "difficulty": "Mixed",
                "url": f"https://www.codechef.com/practice/{topic_key}",
                "category": topic_data['topic_name']
            }
        ]
        
        # Create comprehensive guide entry
        guides[topic_key] = {
            "title": topic_data["topic_name"],
            "video_count": len(youtube_videos),
            "leetcode_count": len(leetcode_problems),
            "codechef_count": len(codechef_problems),
            "estimated_study_time": topic_data.get("study_plan", {}).get("duration", "2-3 weeks"),
            "comprehensive_explanation": f"""
🎯 COMPREHENSIVE {topic_data['topic_name'].upper()} GUIDE

📊 **MULTI-SOURCE LEARNING PATH:**
• 📺 Striver A2Z: {topic_data['striver_content']['total_problems']} problems with optimal solutions
• 📚 Love Babbar: {topic_data['love_babbar_content']['total_problems']} handpicked interview problems  
• 🎯 Aditya Verma: Pattern-based templates and recognition
• 🎓 Apna College: Beginner-friendly step-by-step approach

💻 **C++ IMPLEMENTATIONS:**
{topic_data.get('striver_content', {}).get('content', {}).get('cpp_implementations', {}).get('kadanes_algorithm', 'Advanced C++ implementations available')}

🔥 **KEY PATTERNS TO MASTER:**
{chr(10).join([f'• {pattern}' for pattern in topic_data.get('patterns', [])])}

⚡ **DIFFICULTY PROGRESSION:**
• Beginner: Apna College basics → Love Babbar easy problems
• Intermediate: Aditya Verma patterns → Striver medium problems  
• Advanced: Striver hard problems → Company-specific questions

🎯 **INTERVIEW FOCUS:**
• Total Problems: {topic_data['total_problems']} across all sources
• Must-Know Patterns: {', '.join(topic_data.get('patterns', []))}
• Company Frequency: High (Asked in FAANG+ interviews)

📈 **STUDY PLAN:**
{topic_data.get('study_plan', {}).get('phases', {}).get('Phase 1 (Days 1-5)', {}).get('focus', 'Theory and Basic Understanding')}
            """,
            "youtube_videos": youtube_videos,
            "leetcode_problems": leetcode_problems,
            "codechef_problems": codechef_problems,
            "study_plan": topic_data.get("study_plan", {}),
            "interview_focus": {
                "must_know_problems": [p["name"] for p in leetcode_problems[:5]],
                "common_patterns": topic_data.get("patterns", []),
                "coding_tips": [
                    f"Master {language.upper()} STL for efficient implementations",
                    "Focus on time/space complexity optimization", 
                    "Practice pattern recognition for quick problem solving"
                ]
            }
        }
    
    return {
        "programming_language": language.upper(),
        "total_guides": len(guides),
        "sources": ["Striver A2Z", "Love Babbar 450", "Aditya Verma", "Apna College"],
        "guides": guides
    }:
    from WhatsAppIntegration import (
        send_dsa_progress_to_whatsapp, 
        send_study_guide_to_whatsapp,
        send_scraped_content_to_whatsapp,
        is_whatsapp_configured
    )
    WHATSAPP_ENABLED = True
    print("✅ WhatsApp integration loaded successfully!")
except ImportError as e:
    print(f"⚠️ WhatsApp integration not available: {e}")
    WHATSAPP_ENABLED = False

# Suppress matplotlib font warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*missing from font.*")
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in DSAAgent: {e}")
    client = None

DSA_FILE = r"Data\dsa_progress.json"

# --- HELPER FUNCTIONS ---
def load_dsa_progress():
    try:
        with open(DSA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ DSA progress file not found, creating default...")
        return create_default_progress()

def save_dsa_progress(data):
    try:
        with open(DSA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"❌ Error saving DSA progress: {e}")

def fetch_leetcode_stats(username):
    """Fetch LeetCode stats using GraphQL API"""
    try:
        url = "https://leetcode.com/graphql"
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                submitStats: submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """
        
        response = requests.post(url, json={
            'query': query,
            'variables': {'username': username}
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('matchedUser'):
                stats = data['data']['matchedUser']['submitStats']['acSubmissionNum']
                total = sum(item['count'] for item in stats)
                easy = next((item['count'] for item in stats if item['difficulty'] == 'Easy'), 0)
                medium = next((item['count'] for item in stats if item['difficulty'] == 'Medium'), 0)
                hard = next((item['count'] for item in stats if item['difficulty'] == 'Hard'), 0)
                
                return {
                    'total_solved': total,
                    'easy': {'solved': easy, 'total': 800},
                    'medium': {'solved': medium, 'total': 1600},
                    'hard': {'solved': hard, 'total': 700}
                }
    except Exception as e:
        print(f"❌ Error fetching LeetCode stats: {e}")
    return None

def fetch_codechef_stats(username):
    """Fetch CodeChef stats by scraping profile page"""
    try:
        url = f"https://www.codechef.com/users/{username}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract rating
            rating_elem = soup.find('div', class_='rating-number')
            rating = int(rating_elem.text) if rating_elem and rating_elem.text.isdigit() else 0
            
            # Try multiple selectors for problems solved
            total_solved = 0
            
            # Method 1: Look for problems solved section
            problems_section = soup.find('section', class_='problems-solved')
            if problems_section:
                count_elem = problems_section.find('h3')
                if count_elem:
                    count_text = count_elem.text.strip()
                    if count_text.isdigit():
                        total_solved = int(count_text)
            
            # Method 2: Look for any element with problems count
            if total_solved == 0:
                for elem in soup.find_all(['h3', 'span', 'div']):
                    if elem.text and elem.text.strip().isdigit():
                        num = int(elem.text.strip())
                        if 10 <= num <= 5000:  # Reasonable range for problems solved
                            total_solved = num
                            break
            
            print(f"🔍 CodeChef scraping result: rating={rating}, problems={total_solved}")
            
            # Static override for now - replace with your actual CodeChef problems count
            static_problems = 85  # Update this with your actual CodeChef problems solved
            
            return {
                'total_solved': static_problems,
                'rating': rating,
                'stars': rating // 200
            }
    except Exception as e:
        print(f"❌ Error fetching CodeChef stats: {e}")
    return None

def update_platform_data():
    """Update platform data with real stats"""
    data = load_dsa_progress()
    updated = False
    
    # Update LeetCode
    if data['platforms']['leetcode']['username']:
        print(f"🔄 Fetching LeetCode data for {data['platforms']['leetcode']['username']}...")
        leetcode_stats = fetch_leetcode_stats(data['platforms']['leetcode']['username'])
        if leetcode_stats:
            data['platforms']['leetcode'].update(leetcode_stats)
            updated = True
            print(f"✅ LeetCode: {leetcode_stats['total_solved']} problems")
    
    # Update CodeChef
    if data['platforms']['codechef']['username']:
        print(f"🔄 Fetching CodeChef data for {data['platforms']['codechef']['username']}...")
        codechef_stats = fetch_codechef_stats(data['platforms']['codechef']['username'])
        if codechef_stats:
            data['platforms']['codechef'].update(codechef_stats)
            updated = True
            print(f"✅ CodeChef: {codechef_stats['total_solved']} problems, {codechef_stats['rating']} rating")
    
    if updated:
        save_dsa_progress(data)
        print("📊 Platform data updated successfully!")
    else:
        print("⚠️ No platform data could be fetched")
    
    return data

def create_default_progress():
    # Return the default structure from the JSON file
    return {
        "platforms": {
            "leetcode": {"username": "", "total_solved": 0, "easy": {"solved": 0, "total": 800}, "medium": {"solved": 0, "total": 1600}, "hard": {"solved": 0, "total": 700}, "contest_rating": 0, "streak": 0},
            "codechef": {"username": "", "total_solved": 0, "rating": 0, "stars": 0, "contests_participated": 0, "streak": 0},
            "codeforces": {"username": "", "total_solved": 0, "rating": 0, "rank": "Newbie", "contests_participated": 0, "streak": 0},
            "hackerrank": {"username": "", "total_solved": 0, "badges": 0, "certificates": 0, "streak": 0}
        },
        "topics": {
            "arrays": {"solved": 0, "total": 150, "mastery": 0.0},
            "strings": {"solved": 0, "total": 100, "mastery": 0.0},
            "linked_lists": {"solved": 0, "total": 80, "mastery": 0.0},
            "trees": {"solved": 0, "total": 120, "mastery": 0.0},
            "graphs": {"solved": 0, "total": 100, "mastery": 0.0},
            "dynamic_programming": {"solved": 0, "total": 150, "mastery": 0.0}
        },
        "daily_activity": [],
        "goals": {"daily_target": 3, "weekly_target": 20, "monthly_target": 80}
    }

def update_daily_activity(problems_solved, platforms_used, topics_practiced, time_spent):
    """Update today's DSA activity"""
    data = load_dsa_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if today's entry exists
    today_entry = None
    for entry in data["daily_activity"]:
        if entry["date"] == today:
            today_entry = entry
            break
    
    if today_entry:
        # Update existing entry
        today_entry["problems_solved"] += problems_solved
        today_entry["platforms_used"] = list(set(today_entry["platforms_used"] + platforms_used))
        today_entry["topics_practiced"] = list(set(today_entry["topics_practiced"] + topics_practiced))
        today_entry["time_spent"] += time_spent
    else:
        # Create new entry
        data["daily_activity"].append({
            "date": today,
            "problems_solved": problems_solved,
            "platforms_used": platforms_used,
            "topics_practiced": topics_practiced,
            "time_spent": time_spent
        })
    
    save_dsa_progress(data)
    print(f"📊 Updated DSA activity for {today}")

def calculate_dsa_stats():
    """Calculate comprehensive DSA statistics"""
    data = load_dsa_progress()
    
    # Platform stats
    total_problems = sum(platform["total_solved"] for platform in data["platforms"].values())
    
    # Topic mastery
    topic_stats = []
    for topic, stats in data["topics"].items():
        mastery = (stats["solved"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        topic_stats.append({
            "topic": topic,
            "solved": stats["solved"],
            "total": stats["total"],
            "mastery": mastery
        })
    
    # Recent activity (last 7 days)
    recent_activity = []
    cutoff_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    for activity in data["daily_activity"]:
        if activity["date"] >= cutoff_date:
            recent_activity.append(activity)
    
    weekly_problems = sum(activity["problems_solved"] for activity in recent_activity)
    weekly_time = sum(activity["time_spent"] for activity in recent_activity)
    
    return {
        "total_problems": total_problems,
        "topic_stats": topic_stats,
        "weekly_problems": weekly_problems,
        "weekly_time": weekly_time,
        "platforms": data["platforms"],
        "goals": data["goals"],
        "recent_activity": recent_activity
    }

def generate_dsa_charts():
    """Generate DSA progress charts"""
    data = load_dsa_progress()
    stats = calculate_dsa_stats()
    
    # Create figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f"{Username}'s DSA Progress Dashboard", fontsize=18, fontweight='bold')
    axes = axes.flatten()
    
    # 1. Platform-wise Problems Solved
    ax1 = axes[0]
    platforms = list(data["platforms"].keys())
    problems_solved = [data["platforms"][p]["total_solved"] for p in platforms]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    bars = ax1.bar(platforms, problems_solved, color=colors, alpha=0.8)
    ax1.set_title('Problems Solved by Platform', fontweight='bold')
    ax1.set_ylabel('Problems Solved')
    
    # Add value labels on bars
    for bar, value in zip(bars, problems_solved):
        if value > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    str(value), ha='center', va='bottom', fontweight='bold')
    
    # 2. Topic Mastery Heatmap
    ax2 = axes[1]
    topics = [stat["topic"].replace("_", " ").title() for stat in stats["topic_stats"]]
    mastery_values = [stat["mastery"] for stat in stats["topic_stats"]]
    
    bars = ax2.barh(topics, mastery_values, color='#FF9F43', alpha=0.8)
    ax2.set_title('Topic Mastery (%)', fontweight='bold')
    ax2.set_xlabel('Mastery Percentage')
    ax2.set_xlim(0, 100)
    
    # Add percentage labels
    for bar, value in zip(bars, mastery_values):
        if value > 0:
            ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                    f'{value:.1f}%', ha='left', va='center', fontweight='bold')
    
    # 3. Weekly Activity
    ax3 = axes[2]
    if stats["recent_activity"]:
        dates = [activity["date"] for activity in stats["recent_activity"]]
        daily_problems = [activity["problems_solved"] for activity in stats["recent_activity"]]
        
        ax3.plot(dates, daily_problems, marker='o', linewidth=2, markersize=6, color='#6C5CE7')
        ax3.fill_between(dates, daily_problems, alpha=0.3, color='#6C5CE7')
        ax3.set_title('Daily Problems Solved (Last 7 Days)', fontweight='bold')
        ax3.set_ylabel('Problems Solved')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
    else:
        ax3.text(0.5, 0.5, 'No recent activity data', ha='center', va='center', 
                transform=ax3.transAxes, fontsize=12)
        ax3.set_title('Daily Problems Solved (Last 7 Days)', fontweight='bold')
    
    # 4. Goals Progress
    ax4 = axes[3]
    ax4.axis('off')
    
    # Create progress summary
    goals = data["goals"]
    progress_text = f"""DSA PROGRESS SUMMARY

🎯 GOALS:
• Daily Target: {goals['daily_target']} problems
• Weekly Target: {goals['weekly_target']} problems  
• Monthly Target: {goals['monthly_target']} problems

📊 CURRENT STATS:
• Total Problems: {stats['total_problems']}
• This Week: {stats['weekly_problems']} problems
• Weekly Time: {stats['weekly_time']} minutes

🏆 TOP PLATFORMS:
"""
    
    # Add platform stats
    for platform, data_p in data["platforms"].items():
        if data_p["total_solved"] > 0:
            progress_text += f"• {platform.title()}: {data_p['total_solved']} problems\n"
    
    ax4.text(0.1, 0.9, progress_text, transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Save chart
    chart_path = r"Data\dsa_analysis.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_path

def load_study_guides():
    """Load study guides from JSON file - prefer enhanced version"""
    try:
        # Try enhanced study guides first
        with open(r"Data\dsa_study_guides_enhanced.json", 'r', encoding='utf-8') as f:
            enhanced_data = json.load(f)
            print("✅ Loading enhanced study guides with comprehensive content!")
            return enhanced_data
    except FileNotFoundError:
        try:
            # Fallback to basic study guides
            with open(r"Data\dsa_study_guides.json", 'r', encoding='utf-8') as f:
                print("⚠️ Using basic study guides - enhance with enhanced_dsa_content_scraper.py")
                return json.load(f)
        except FileNotFoundError:
            return {"programming_language": "Python", "guides": {}}

def get_language_preference(query):
    """Detect or ask for programming language preference"""
    query_lower = query.lower()
    
    # Check if language is mentioned in query
    if 'python' in query_lower or 'py' in query_lower:
        return 'Python'
    elif 'java' in query_lower:
        return 'Java'
    elif 'c++' in query_lower or 'cpp' in query_lower:
        return 'C++'
    elif 'javascript' in query_lower or 'js' in query_lower:
        return 'JavaScript'
    
    # If no language mentioned, return None to prompt user
    return None

def update_language_preference(language):
    """Update the programming language preference in the JSON file"""
    try:
        guides_data = load_study_guides()
        guides_data["programming_language"] = language
        with open(r"Data\dsa_study_guides.json", 'w', encoding='utf-8') as f:
            json.dump(guides_data, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error updating language preference: {e}")
        return False

def generate_topic_guide(topic, query=""):
    """Generate study guide for specific DSA topic"""
    guides_data = load_study_guides()
    guides = guides_data.get("guides", {})
    
    # Check for language preference
    preferred_lang = get_language_preference(query)
    if preferred_lang:
        update_language_preference(preferred_lang)
        lang = preferred_lang
    else:
        lang = guides_data.get("programming_language", "Python")
        # If no language set, ask user
        if lang == "Python" and "python" not in query.lower():
            return """🔤 LANGUAGE PREFERENCE

Which programming language would you like to focus on?

• "arrays guide in Python"
• "trees guide in Java" 
• "graphs guide in C++"
• "DP guide in JavaScript"

Or just say: "set language to Python/Java/C++/JavaScript"

I'll remember your preference for future guides!"""
    
    if topic not in guides:
        topic = 'arrays'  # Default fallback
    
    guide = guides[topic]
    topic_name = guide.get("title", topic.replace('_', ' ').title())
    
    # Check if this is enhanced guide format
    is_enhanced = 'video_count' in guide and 'comprehensive_explanation' in guide
    
    if is_enhanced:
        # Format enhanced YouTube videos with more details
        youtube_section = "\n".join([
            f"• {video['title']} - {video['channel']} ({video.get('duration', 'N/A')})\n  🎯 Difficulty: {video.get('difficulty', 'All levels')}\n  📝 Topics: {', '.join(video.get('topics_covered', []))}\n  🔗 {video['url']}"
            for video in guide.get('youtube_videos', [])
        ])
        
        # Format enhanced LeetCode problems with patterns
        leetcode_section = "\n".join([
            f"• {problem['name']} ({problem['difficulty']}) - Pattern: {problem.get('pattern', 'General')}\n  🔗 {problem['url']}"
            for problem in guide.get('leetcode_problems', [])
        ])
        
        # Format enhanced CodeChef problems with categories
        codechef_section = "\n".join([
            f"• {problem['name']} ({problem['difficulty']}) - {problem.get('category', 'General')}\n  🔗 {problem['url']}"
            for problem in guide.get('codechef_problems', [])
        ])
        
        # Get enhanced details
        study_time = guide.get('estimated_study_time', '8-12 hours')
        video_count = guide.get('video_count', 0)
        leetcode_count = guide.get('leetcode_count', 0)
        codechef_count = guide.get('codechef_count', 0)
        
        # Get study plan
        study_plan = guide.get('study_plan', {})
        study_plan_text = "\n".join([
            f"Week {week[-1]}: {plan}" for week, plan in study_plan.items()
        ]) if study_plan else "Follow structured approach: Theory → Easy Problems → Medium Problems → Hard Problems"
        
        # Get interview focus
        interview_focus = guide.get('interview_focus', {})
        must_know = interview_focus.get('must_know_problems', [])
        patterns = interview_focus.get('common_patterns', [])
        tips = interview_focus.get('coding_tips', [])
        
        enhanced_content = f"""
🎯 {topic_name} STUDY GUIDE - ENHANCED EDITION
💻 Programming Language: {lang}
⏱️ Estimated Study Time: {study_time}
📊 Content: {video_count} videos, {leetcode_count} LeetCode, {codechef_count} CodeChef problems

📺 COMPREHENSIVE YOUTUBE VIDEOS ({video_count} videos):
{youtube_section}

💻 LEETCODE PROBLEMS ({leetcode_count} problems):
{leetcode_section}

🏆 CODECHEF PROBLEMS ({codechef_count} problems):
{codechef_section}

📚 STRUCTURED STUDY PLAN:
{study_plan_text}

🎯 INTERVIEW PREPARATION:
📋 Must-Know Problems: {', '.join(must_know[:3]) + '...' if len(must_know) > 3 else ', '.join(must_know)}
🔑 Key Patterns: {', '.join(patterns)}

💡 CODING TIPS:
{chr(10).join([f'• {tip}' for tip in tips])}

🚀 ADDITIONAL RESOURCES:
• GeeksforGeeks: Comprehensive articles and examples
• CP-Algorithms: Advanced algorithmic concepts  
• LeetCode Explore: Interactive learning paths

💪 Ready to master {topic_name}? Start with Week 1 and work systematically!"""
        
        return enhanced_content
    
    else:
        # Original format for basic guides
        youtube_section = "\n".join([
            f"• {video['title']} - {video['channel']} ({video['duration']})\n  🔗 {video['url']}"
            for video in guide.get('youtube_videos', [])
        ])
        
        leetcode_section = "\n".join([
            f"• {problem['name']} ({problem['difficulty']})\n  🔗 {problem['url']}"
            for problem in guide.get('leetcode_problems', [])
        ])
        
        codechef_section = "\n".join([
            f"• {problem['name']} ({problem['difficulty']})\n  🔗 {problem['url']}"
            for problem in guide.get('codechef_problems', [])
        ])
        
        return f"""🎯 {topic_name} STUDY GUIDE
💻 Programming Language: {lang}

📺 RECOMMENDED YOUTUBE VIDEOS:
{youtube_section}

💻 LEETCODE PROBLEMS:
{leetcode_section}

🏆 CODECHEF PROBLEMS:
{codechef_section}

📚 STUDY PLAN:
1. Watch YouTube videos for theory and concepts
2. Solve LeetCode problems for interview prep
3. Practice CodeChef problems for competitive programming
4. Code in {lang} and optimize solutions
5. Track progress in your DSA dashboard

💡 TIP: Follow Striver's A2Z DSA sheet for structured learning!
⚠️ Note: Upgrade to enhanced guides with 'python enhanced_dsa_content_scraper.py'"""
    
    # 🚀 NEW: Send study guide to WhatsApp if configured
    if WHATSAPP_ENABLED and is_whatsapp_configured():
        print(f"📱 Sending {topic_name} study guide to WhatsApp...")
        guide_data = {
            'youtube_videos': guide.get('youtube_videos', []),
            'leetcode_problems': guide.get('leetcode_problems', []),
            'codechef_problems': guide.get('codechef_problems', []),
            'key_concepts': [
                f"Programming Language: {lang}",
                "Watch videos for concepts",
                "Solve problems for practice",
                "Track progress regularly"
            ]
        }
        whatsapp_sent = send_study_guide_to_whatsapp(topic, guide_data)
        
        if whatsapp_sent:
            return f"""{topic_name} STUDY GUIDE
💻 Programming Language: {lang}

📺 RECOMMENDED YOUTUBE VIDEOS:
{youtube_section}

💻 LEETCODE PROBLEMS:
{leetcode_section}

🏆 CODECHEF PROBLEMS:
{codechef_section}

📚 STUDY PLAN:
1. Watch YouTube videos for theory and concepts
2. Solve LeetCode problems for interview prep
3. Practice CodeChef problems for competitive programming
4. Code in {lang} and optimize solutions
5. Track progress in your DSA dashboard

💡 TIP: Follow Striver's A2Z DSA sheet for structured learning!

📱 Study guide sent to your WhatsApp!"""
        else:
            return f"""🎯 {topic_name} STUDY GUIDE
💻 Programming Language: {lang}

📺 RECOMMENDED YOUTUBE VIDEOS:
{youtube_section}

💻 LEETCODE PROBLEMS:
{leetcode_section}

🏆 CODECHEF PROBLEMS:
{codechef_section}

📚 STUDY PLAN:
1. Watch YouTube videos for theory and concepts
2. Solve LeetCode problems for interview prep
3. Practice CodeChef problems for competitive programming
4. Code in {lang} and optimize solutions
5. Track progress in your DSA dashboard

💡 TIP: Follow Striver's A2Z DSA sheet for structured learning!

⚠️ Could not send to WhatsApp (check your phone number in .env)"""
    elif WHATSAPP_ENABLED:
        return f"""🎯 {topic_name} STUDY GUIDE
💻 Programming Language: {lang}

📺 RECOMMENDED YOUTUBE VIDEOS:
{youtube_section}

💻 LEETCODE PROBLEMS:
{leetcode_section}

🏆 CODECHEF PROBLEMS:
{codechef_section}

📚 STUDY PLAN:
1. Watch YouTube videos for theory and concepts
2. Solve LeetCode problems for interview prep
3. Practice CodeChef problems for competitive programming
4. Code in {lang} and optimize solutions
5. Track progress in your DSA dashboard

💡 TIP: Follow Striver's A2Z DSA sheet for structured learning!

💡 Tip: Set USER_PHONE in .env to receive study guides on WhatsApp!"""
    
    # Return original guide if WhatsApp not enabled
    return f"""🎯 {topic_name} STUDY GUIDE
💻 Programming Language: {lang}

📺 RECOMMENDED YOUTUBE VIDEOS:
{youtube_section}

💻 LEETCODE PROBLEMS:
{leetcode_section}

🏆 CODECHEF PROBLEMS:
{codechef_section}

📚 STUDY PLAN:
1. Watch YouTube videos for theory and concepts
2. Solve LeetCode problems for interview prep
3. Practice CodeChef problems for competitive programming
4. Code in {lang} and optimize solutions
5. Track progress in your DSA dashboard

💡 TIP: Follow Striver's A2Z DSA sheet for structured learning!"""

def DSAAgent(query: str):
    """Main DSA Agent function"""
    if not client:
        return "DSA analysis is not available due to AI model configuration issues."
    
    # Handle empty or malformed queries
    if not query or query.strip() in ['(query)', '']:
        query = "show my progress"
    
    query_lower = query.lower()
    
    # Handle different DSA commands
    
    # 🚀 NEW: WhatsApp-specific commands
    if "whatsapp" in query_lower or "send to whatsapp" in query_lower:
        if not WHATSAPP_ENABLED:
            return "❌ WhatsApp integration is not available. Please install pywhatkit."
        
        if not is_whatsapp_configured():
            return """❌ WhatsApp not configured! 

To enable WhatsApp integration:
1. Add your phone number to .env file:
   USER_PHONE=+1234567890
2. Include country code (e.g., +91 for India, +1 for US)
3. Restart NEXUS

Commands available after setup:
• "send progress to whatsapp"
• "whatsapp my dsa summary" 
• "send arrays guide to whatsapp"
"""
        
        # Check for study guide commands first (more specific)
        if "guide" in query_lower or "study" in query_lower:
            # Send study guide to WhatsApp
            topics = ['arrays', 'strings', 'linked_lists', 'trees', 'graphs', 'dynamic_programming']
            topic = None
            for t in topics:
                if t.replace('_', ' ') in query_lower or t in query_lower:
                    topic = t
                    break
            
            if not topic:
                topic = 'arrays'  # Default
            
            try:
                print(f"📱 Preparing {topic} study guide for WhatsApp...")
                guides_data = load_study_guides()
                guide = guides_data.get("guides", {}).get(topic, {})
                
                guide_data = {
                    'youtube_videos': guide.get('youtube_videos', []),
                    'leetcode_problems': guide.get('leetcode_problems', []),
                    'codechef_problems': guide.get('codechef_problems', []),
                    'key_concepts': [
                        "Watch videos for concepts",
                        "Solve problems for practice", 
                        "Track progress regularly"
                    ]
                }
                
                whatsapp_sent = send_study_guide_to_whatsapp(topic, guide_data)
                if whatsapp_sent:
                    return f"✅ {topic.replace('_', ' ').title()} study guide scheduled for WhatsApp! Check your phone in ~5 minutes."
                else:
                    return "❌ Failed to send study guide to WhatsApp. Please check your phone number configuration."
            except Exception as e:
                return f"❌ Error sending study guide to WhatsApp: {e}"
        
        elif "progress" in query_lower or "summary" in query_lower:
            # Send progress to WhatsApp
            try:
                print("📱 Preparing DSA progress for WhatsApp...")
                update_platform_data()
                dsa_data = load_dsa_progress()
                
                whatsapp_sent = send_dsa_progress_to_whatsapp(dsa_data)
                if whatsapp_sent:
                    return "✅ DSA progress report scheduled for WhatsApp! Check your phone in ~5 minutes."
                else:
                    return "❌ Failed to send to WhatsApp. Please check your phone number configuration."
            except Exception as e:
                return f"❌ Error sending to WhatsApp: {e}"
        
        elif any(topic in query_lower for topic in ['arrays', 'strings', 'trees', 'graphs', 'dynamic']):
            # Fallback for topic-specific queries without explicit "guide" keyword
            return """📱 Did you mean to request a study guide?

Try these specific commands:
• "send arrays guide to whatsapp"
• "send trees guide to whatsapp"  
• "send dynamic programming guide to whatsapp"

Or for progress reports:
• "send progress to whatsapp"
• "whatsapp my dsa summary"
"""
        
        else:
            return """📱 WhatsApp DSA Commands:

• "send progress to whatsapp" - Send full DSA progress report
• "whatsapp my dsa summary" - Send progress summary
• "send arrays guide to whatsapp" - Send arrays study guide
• "whatsapp trees study guide" - Send trees guide
• "send dynamic programming guide to whatsapp" - Send DP guide

Available topics: arrays, strings, trees, graphs, dynamic programming
"""
    
    elif "progress" in query_lower or "summary" in query_lower:
        try:
            # Update with real data first
            print("🔄 Updating platform data...")
            update_platform_data()
            
            stats = calculate_dsa_stats()
            chart_path = generate_dsa_charts()
            
            summary = f"""
🧠 DSA PROGRESS SUMMARY for {Username}

📊 OVERALL STATS:
• Total Problems Solved: {stats['total_problems']}
• Weekly Problems: {stats['weekly_problems']}
• Weekly Study Time: {stats['weekly_time']} minutes

🏆 PLATFORM BREAKDOWN:
"""
            for platform, data in stats['platforms'].items():
                if data['total_solved'] > 0:
                    summary += f"• {platform.title()}: {data['total_solved']} problems\n"
            
            summary += f"\n📈 Charts saved to: {chart_path}"
            
            # 🚀 NEW: Send progress to WhatsApp if configured
            if WHATSAPP_ENABLED and is_whatsapp_configured():
                print("📱 Sending DSA progress to WhatsApp...")
                dsa_data = load_dsa_progress()
                whatsapp_sent = send_dsa_progress_to_whatsapp(dsa_data)
                if whatsapp_sent:
                    summary += "\n📱 Progress report sent to your WhatsApp!"
                else:
                    summary += "\n⚠️ Could not send to WhatsApp (check your phone number in .env)"
            elif WHATSAPP_ENABLED:
                summary += "\n💡 Tip: Set USER_PHONE in .env to receive progress on WhatsApp!"
            
            return summary
            
        except Exception as e:
            return f"Error generating DSA summary: {e}"
    
    elif "guide" in query_lower or "prep" in query_lower or "study" in query_lower:
        # Extract topic if mentioned
        topics = ['arrays', 'strings', 'linked_lists', 'trees', 'graphs', 'dynamic_programming', 'greedy', 'backtracking', 'binary_search', 'sorting']
        topic = None
        for t in topics:
            if t.replace('_', ' ') in query_lower or t in query_lower:
                topic = t
                break
        
        if topic:
            return generate_topic_guide(topic, query)
        else:
            return """🎯 DSA PREP GUIDE

Specify a topic for personalized study plan:
• "arrays guide" - Array problems & videos
• "trees prep" - Tree algorithms & practice
• "dynamic programming study" - DP concepts & problems
• "graphs guide" - Graph theory & implementation

Available topics: Arrays, Strings, Linked Lists, Trees, Graphs, Dynamic Programming, Greedy, Backtracking, Binary Search, Sorting"""
    
    elif "set language" in query_lower or "language to" in query_lower:
        # Handle language setting
        if "python" in query_lower:
            lang = "Python"
        elif "java" in query_lower:
            lang = "Java"
        elif "c++" in query_lower or "cpp" in query_lower:
            lang = "C++"
        elif "javascript" in query_lower or "js" in query_lower:
            lang = "JavaScript"
        else:
            return """🔤 LANGUAGE OPTIONS

Supported languages:
• Python
• Java
• C++
• JavaScript

Say: "set language to Python" (or your preferred language)"""
        
        if update_language_preference(lang):
            return f"✅ Language preference set to {lang}! All future DSA guides will focus on {lang}."
        else:
            return "❌ Failed to update language preference."
    
    elif "analyze code" in query_lower or "code review" in query_lower or "code quality" in query_lower:
        try:
            from Backend.code_quality_analyzer import DSACodeAnalyzer
            
            # Ask for code input
            return """📝 **CODE QUALITY ANALYZER**

Please provide your code for analysis. You can:

1. **Paste your code directly** in the next message
2. **Specify problem name** for context (optional)
3. **Mention language** if not Python

Example:
```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return None
```

I'll analyze:
• ⏱️ Time complexity
• 🧠 Code complexity
• 📊 Maintainability score
• 💡 Optimization suggestions
• 🎯 Overall rating

**Ready for your code!**"""
            
        except ImportError:
            return "❌ Code quality analyzer not available. Please install required dependencies."
    
    elif "add" in query_lower or "log" in query_lower:
        return """To log your DSA progress, tell me:
        
🔢 "I solved 3 problems on leetcode today"
📚 "Practiced arrays and strings for 2 hours"
🏆 "Completed 5 problems on codeforces"

I'll track your progress across all platforms!"""
    
    else:
        # General DSA advice using AI
        context = f"DSA Progress Data: {calculate_dsa_stats()}"
        
        system_prompt = f"You are Nexus, {Username}'s DSA mentor. Provide coding interview advice with wit."
        
        messages_to_send = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages_to_send,
                max_tokens=1024,
                temperature=0.7,
                stream=False
            )
            
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error in DSAAgent: {e}")
            return "I'm having trouble with DSA analysis right now."

# --- TESTING ---
if __name__ == "__main__":
    print("DSAAgent test. Type 'exit' to end.")
    while True:
        user_input = input(f"{Username}: ")
        if user_input.lower() == 'exit':
            break
        response = DSAAgent(user_input)
        print(f"Nexus: {response}")