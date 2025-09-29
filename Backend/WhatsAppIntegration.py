# Backend/WhatsAppIntegration.py

import pywhatkit as kit
import json
from datetime import datetime, timedelta
from dotenv import dotenv_values
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
USERNAME = env_vars.get("Username", "User")
USER_PHONE = env_vars.get("USER_PHONE", "")  # User's WhatsApp number

def send_whatsapp_message(phone_number, message, delay_minutes=2):
    """
    Send WhatsApp message using pywhatkit
    
    Args:
        phone_number (str): Phone number with country code (e.g., "+919876543210")
        message (str): Message to send
        delay_minutes (int): Minutes to wait before sending (default: 2)
    
    Returns:
        bool: True if scheduled successfully, False otherwise
    """
    try:
        # Calculate send time (current time + delay)
        send_time = datetime.now() + timedelta(minutes=delay_minutes)
        hour = send_time.hour
        minute = send_time.minute
        
        print(f"📱 Scheduling WhatsApp message to {phone_number}")
        print(f"⏰ Message will be sent at {hour:02d}:{minute:02d}")
        
        # Schedule the message with longer wait time
        kit.sendwhatmsg(phone_number, message, hour, minute, wait_time=20, tab_close=True)
        
        print("✅ WhatsApp message scheduled successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error scheduling WhatsApp message: {e}")
        return False

def format_dsa_progress_message(dsa_data):
    """
    Format DSA progress data into a WhatsApp-friendly message
    
    Args:
        dsa_data (dict): DSA progress data
    
    Returns:
        str: Formatted message
    """
    try:
        message = f"🚀 *NEXUS DSA Progress Report* 📊\n\n"
        message += f"Hi {USERNAME}! Here's your coding progress:\n\n"
        
        # Platform Statistics
        message += "*📱 PLATFORM STATS:*\n"
        platforms = dsa_data.get('platforms', {})
        
        if platforms.get('leetcode', {}).get('username'):
            lc = platforms['leetcode']
            message += f"🔥 *LeetCode:* {lc.get('total_solved', 0)} problems\n"
            message += f"   Easy: {lc.get('easy', {}).get('solved', 0)}/{lc.get('easy', {}).get('total', 0)}\n"
            message += f"   Medium: {lc.get('medium', {}).get('solved', 0)}/{lc.get('medium', {}).get('total', 0)}\n"
            message += f"   Hard: {lc.get('hard', {}).get('solved', 0)}/{lc.get('hard', {}).get('total', 0)}\n"
            if lc.get('contest_rating', 0) > 0:
                message += f"   Rating: {lc.get('contest_rating', 0)}\n"
        
        if platforms.get('codechef', {}).get('username'):
            cc = platforms['codechef']
            message += f"👨‍🍳 *CodeChef:* {cc.get('total_solved', 0)} problems\n"
            message += f"   Rating: {cc.get('rating', 0)} ⭐\n"
            message += f"   Stars: {cc.get('stars', 0)}\n"
        
        if platforms.get('codeforces', {}).get('username'):
            cf = platforms['codeforces']
            message += f"⚔️ *Codeforces:* {cf.get('total_solved', 0)} problems\n"
            message += f"   Rating: {cf.get('rating', 0)} ({cf.get('rank', 'Unrated')})\n"
        
        # Topic Mastery
        message += "\n*🎯 TOPIC MASTERY:*\n"
        topics = dsa_data.get('topics', {})
        
        for topic, data in topics.items():
            solved = data.get('solved', 0)
            total = data.get('total', 0)
            mastery = data.get('mastery', 0.0) * 100
            topic_name = topic.replace('_', ' ').title()
            message += f"📚 {topic_name}: {solved}/{total} ({mastery:.1f}%)\n"
        
        # Daily Activity (Last 7 days)
        daily_activity = dsa_data.get('daily_activity', [])
        if daily_activity:
            message += "\n*📈 RECENT ACTIVITY:*\n"
            recent_activity = daily_activity[-7:]  # Last 7 days
            total_recent = sum(entry.get('problems_solved', 0) for entry in recent_activity)
            message += f"Last 7 days: {total_recent} problems solved\n"
        
        # Goals Progress
        goals = dsa_data.get('goals', {})
        message += "\n*🎯 GOALS:*\n"
        message += f"Daily Target: {goals.get('daily_target', 3)} problems\n"
        message += f"Weekly Target: {goals.get('weekly_target', 20)} problems\n"
        message += f"Monthly Target: {goals.get('monthly_target', 80)} problems\n"
        
        message += f"\n💪 Keep coding! You're doing great!\n"
        message += f"📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        message += "*Powered by NEXUS AI Career Acceleration System* 🚀"
        
        return message
        
    except Exception as e:
        print(f"❌ Error formatting DSA message: {e}")
        return f"Hi {USERNAME}! Your DSA progress report is ready, but there was an error formatting it. Please check the NEXUS dashboard for details."

def format_study_guide_message(topic, guide_data):
    """
    Format study guide data into WhatsApp message
    
    Args:
        topic (str): Topic name (e.g., 'arrays', 'trees')
        guide_data (dict): Study guide data
    
    Returns:
        str: Formatted message
    """
    try:
        topic_name = topic.replace('_', ' ').title()
        message = f"📚 *NEXUS Study Guide: {topic_name}* 🎯\n\n"
        message += f"Hi {USERNAME}! Here's your personalized study guide:\n\n"
        
        # YouTube Videos
        if 'youtube_videos' in guide_data:
            message += "*📺 RECOMMENDED VIDEOS:*\n"
            for video in guide_data['youtube_videos'][:3]:  # Top 3 videos
                title = video.get('title', 'Video')
                duration = video.get('duration', '')
                url = video.get('url', '')
                message += f"• {title}"
                if duration:
                    message += f" ({duration})"
                message += f"\n  🔗 {url}\n\n"
        
        # Practice Problems
        if 'leetcode_problems' in guide_data:
            message += "*💻 PRACTICE PROBLEMS:*\n"
            for problem in guide_data['leetcode_problems'][:5]:  # Top 5 problems
                name = problem.get('name', 'Problem')
                difficulty = problem.get('difficulty', 'Unknown')
                url = problem.get('url', '')
                message += f"• {name} ({difficulty})\n"
                if url:
                    message += f"  🔗 {url}\n"
        
        # Key Concepts
        if 'key_concepts' in guide_data:
            message += "\n*🧠 KEY CONCEPTS:*\n"
            for concept in guide_data['key_concepts'][:5]:
                message += f"• {concept}\n"
        
        message += f"\n📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        message += "*Happy Learning! 🚀*\n\n"
        message += "*Powered by NEXUS AI Career Acceleration System*"
        
        return message
        
    except Exception as e:
        print(f"❌ Error formatting study guide message: {e}")
        return f"Hi {USERNAME}! Your {topic} study guide is ready. Please check the NEXUS dashboard for details."

def send_dsa_progress_to_whatsapp(dsa_data, phone_number=None):
    """
    Send DSA progress report to WhatsApp
    
    Args:
        dsa_data (dict): DSA progress data
        phone_number (str): Phone number (optional, uses env variable if not provided)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        target_phone = phone_number or USER_PHONE
        
        if not target_phone:
            print("❌ No phone number configured. Please set USER_PHONE in .env file")
            return False
        
        message = format_dsa_progress_message(dsa_data)
        return send_whatsapp_message(target_phone, message, delay_minutes=2)
        
    except Exception as e:
        print(f"❌ Error sending DSA progress to WhatsApp: {e}")
        return False

def send_study_guide_to_whatsapp(topic, guide_data, phone_number=None):
    """
    Send study guide to WhatsApp
    
    Args:
        topic (str): Topic name
        guide_data (dict): Study guide data
        phone_number (str): Phone number (optional, uses env variable if not provided)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        target_phone = phone_number or USER_PHONE
        
        if not target_phone:
            print("❌ No phone number configured. Please set USER_PHONE in .env file")
            return False
        
        message = format_study_guide_message(topic, guide_data)
        return send_whatsapp_message(target_phone, message, delay_minutes=2)
        
    except Exception as e:
        print(f"❌ Error sending study guide to WhatsApp: {e}")
        return False

def send_scraped_content_to_whatsapp(content_title, scraped_data, phone_number=None):
    """
    Send any scraped content to WhatsApp
    
    Args:
        content_title (str): Title of the scraped content
        scraped_data (str or dict): Scraped content data
        phone_number (str): Phone number (optional, uses env variable if not provided)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        target_phone = phone_number or USER_PHONE
        
        if not target_phone:
            print("❌ No phone number configured. Please set USER_PHONE in .env file")
            return False
        
        # Format the scraped content message
        message = f"🔍 *NEXUS Scraped Content* 📊\n\n"
        message += f"Hi {USERNAME}! Here's your requested content:\n\n"
        message += f"*📋 {content_title}*\n\n"
        
        # Handle different data types
        if isinstance(scraped_data, dict):
            for key, value in scraped_data.items():
                message += f"*{key.replace('_', ' ').title()}:* {value}\n"
        elif isinstance(scraped_data, str):
            # Truncate if too long for WhatsApp
            if len(scraped_data) > 1000:
                message += scraped_data[:1000] + "...\n\n*[Content truncated for WhatsApp]*"
            else:
                message += scraped_data
        else:
            message += str(scraped_data)
        
        message += f"\n\n📅 Scraped: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        message += "*Powered by NEXUS AI Career Acceleration System* 🚀"
        
        return send_whatsapp_message(target_phone, message, delay_minutes=2)
        
    except Exception as e:
        print(f"❌ Error sending scraped content to WhatsApp: {e}")
        return False

# --- UTILITY FUNCTIONS ---

def is_whatsapp_configured():
    """Check if WhatsApp integration is properly configured"""
    return bool(USER_PHONE)

def get_user_phone():
    """Get user's phone number from environment"""
    return USER_PHONE

def test_whatsapp_integration():
    """Test WhatsApp integration with a simple message"""
    if not is_whatsapp_configured():
        print("❌ WhatsApp not configured. Please set USER_PHONE in .env file")
        return False
    
    test_message = f"🚀 NEXUS WhatsApp Integration Test\n\nHi {USERNAME}!\n\nThis is a test message from your NEXUS AI system.\n\nIf you received this, WhatsApp integration is working perfectly! 🎉\n\n*Powered by NEXUS AI Career Acceleration System*"
    
    return send_whatsapp_message(USER_PHONE, test_message, delay_minutes=2)

if __name__ == "__main__":
    # Test the integration
    print("🧪 Testing WhatsApp Integration...")
    test_whatsapp_integration()