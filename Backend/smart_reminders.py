#!/usr/bin/env python3
"""
Smart Reminder System for NEXUS AI Assistant
"""

import json
import os
from datetime import datetime, timedelta
import threading
import time
from typing import List, Dict, Optional

class SmartReminderSystem:
    def __init__(self):
        self.reminders_file = "Data/reminders.json"
        self.reminders = self.load_reminders()
        self.running = False
        self.reminder_thread = None
        
    def load_reminders(self) -> List[Dict]:
        """Load reminders from file"""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading reminders: {e}")
            return []
    
    def save_reminders(self):
        """Save reminders to file"""
        try:
            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(self.reminders, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving reminders: {e}")
    
    def add_reminder(self, title: str, message: str, reminder_time: str, 
                    reminder_type: str = "general", repeat: Optional[str] = None) -> str:
        """Add a new reminder"""
        try:
            # Parse reminder time
            if reminder_time.lower() in ["now", "immediately"]:
                target_time = datetime.now()
            else:
                # Try to parse different time formats
                target_time = self.parse_time(reminder_time)
            
            reminder = {
                "id": len(self.reminders) + 1,
                "title": title,
                "message": message,
                "reminder_time": target_time.isoformat(),
                "type": reminder_type,
                "repeat": repeat,
                "status": "active",
                "created": datetime.now().isoformat()
            }
            
            self.reminders.append(reminder)
            self.save_reminders()
            
            return f"✅ Reminder set: '{title}' for {target_time.strftime('%Y-%m-%d %H:%M')}"
            
        except Exception as e:
            return f"❌ Error setting reminder: {e}"
    
    def parse_time(self, time_str: str) -> datetime:
        """Parse various time formats"""
        time_str = time_str.lower().strip()
        now = datetime.now()
        
        # Handle relative times
        if "in" in time_str:
            if "minute" in time_str:
                minutes = int([word for word in time_str.split() if word.isdigit()][0])
                return now + timedelta(minutes=minutes)
            elif "hour" in time_str:
                hours = int([word for word in time_str.split() if word.isdigit()][0])
                return now + timedelta(hours=hours)
            elif "day" in time_str:
                days = int([word for word in time_str.split() if word.isdigit()][0])
                return now + timedelta(days=days)
        
        # Handle specific times today
        if "at" in time_str:
            time_part = time_str.split("at")[-1].strip()
            try:
                hour, minute = map(int, time_part.replace(":", " ").split()[:2])
                return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            except:
                pass
        
        # Handle tomorrow
        if "tomorrow" in time_str:
            if "at" in time_str:
                time_part = time_str.split("at")[-1].strip()
                try:
                    hour, minute = map(int, time_part.replace(":", " ").split()[:2])
                    return (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
                except:
                    pass
            return now + timedelta(days=1)
        
        # Default: try to parse as standard datetime format
        try:
            return datetime.fromisoformat(time_str)
        except:
            # Fallback: 1 hour from now
            return now + timedelta(hours=1)
    
    def get_due_reminders(self) -> List[Dict]:
        """Get reminders that are due"""
        due_reminders = []
        now = datetime.now()
        
        for reminder in self.reminders:
            if reminder["status"] != "active":
                continue
                
            reminder_time = datetime.fromisoformat(reminder["reminder_time"])
            if now >= reminder_time:
                due_reminders.append(reminder)
        
        return due_reminders
    
    def mark_reminder_completed(self, reminder_id: int):
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                reminder["status"] = "completed"
                reminder["completed_at"] = datetime.now().isoformat()
                break
        self.save_reminders()
    
    def snooze_reminder(self, reminder_id: int, snooze_minutes: int = 10):
        """Snooze a reminder"""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                current_time = datetime.fromisoformat(reminder["reminder_time"])
                new_time = current_time + timedelta(minutes=snooze_minutes)
                reminder["reminder_time"] = new_time.isoformat()
                break
        self.save_reminders()
    
    def list_active_reminders(self) -> str:
        """List all active reminders"""
        active_reminders = [r for r in self.reminders if r["status"] == "active"]
        
        if not active_reminders:
            return "📅 No active reminders"
        
        result = "📅 ACTIVE REMINDERS:\n\n"
        for reminder in active_reminders:
            reminder_time = datetime.fromisoformat(reminder["reminder_time"])
            time_diff = reminder_time - datetime.now()
            
            if time_diff.total_seconds() > 0:
                if time_diff.days > 0:
                    time_str = f"in {time_diff.days} days"
                elif time_diff.seconds > 3600:
                    hours = time_diff.seconds // 3600
                    time_str = f"in {hours} hours"
                else:
                    minutes = time_diff.seconds // 60
                    time_str = f"in {minutes} minutes"
            else:
                time_str = "⚠️ OVERDUE"
            
            result += f"🔔 **{reminder['title']}** (ID: {reminder['id']})\n"
            result += f"   📝 {reminder['message']}\n"
            result += f"   ⏰ {reminder_time.strftime('%Y-%m-%d %H:%M')} ({time_str})\n"
            result += f"   🏷️ Type: {reminder['type']}\n\n"
        
        return result
    
    def start_monitoring(self):
        """Start the reminder monitoring thread"""
        if not self.running:
            self.running = True
            self.reminder_thread = threading.Thread(target=self._monitor_reminders, daemon=True)
            self.reminder_thread.start()
            print("🔔 Reminder monitoring started")
    
    def stop_monitoring(self):
        """Stop the reminder monitoring"""
        self.running = False
        print("🔔 Reminder monitoring stopped")
    
    def _monitor_reminders(self):
        """Monitor reminders in background thread"""
        while self.running:
            try:
                due_reminders = self.get_due_reminders()
                
                for reminder in due_reminders:
                    self._trigger_reminder(reminder)
                    
                    # Handle repeat reminders
                    if reminder.get("repeat"):
                        self._schedule_repeat(reminder)
                    else:
                        self.mark_reminder_completed(reminder["id"])
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"❌ Error in reminder monitoring: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _trigger_reminder(self, reminder: Dict):
        """Trigger a reminder notification"""
        print(f"\n🔔 REMINDER: {reminder['title']}")
        print(f"📝 {reminder['message']}")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        
        # You could add sound notification, desktop notification, etc. here
        # For now, just print to console
    
    def _schedule_repeat(self, reminder: Dict):
        """Schedule a repeat reminder"""
        repeat = reminder["repeat"]
        current_time = datetime.fromisoformat(reminder["reminder_time"])
        
        if repeat == "daily":
            new_time = current_time + timedelta(days=1)
        elif repeat == "weekly":
            new_time = current_time + timedelta(weeks=1)
        elif repeat == "monthly":
            new_time = current_time + timedelta(days=30)
        else:
            return  # Unknown repeat type
        
        reminder["reminder_time"] = new_time.isoformat()
        self.save_reminders()

# Global instance
reminder_system = SmartReminderSystem()

def ReminderAgent(query: str) -> str:
    """Process reminder-related queries"""
    query = query.lower().strip()
    
    if "set reminder" in query or "remind me" in query:
        # Extract reminder details
        try:
            if "to" in query:
                parts = query.split("to", 1)
                if len(parts) == 2:
                    title_part = parts[1].strip()
                    if "at" in title_part or "in" in title_part:
                        # Extract time
                        time_keywords = ["at", "in"]
                        for keyword in time_keywords:
                            if keyword in title_part:
                                title, time_part = title_part.split(keyword, 1)
                                title = title.strip()
                                time_str = keyword + " " + time_part.strip()
                                return reminder_system.add_reminder(
                                    title=title,
                                    message=f"Reminder: {title}",
                                    reminder_time=time_str
                                )
                        
                        # Default case
                        return reminder_system.add_reminder(
                            title=title_part,
                            message=f"Reminder: {title_part}",
                            reminder_time="in 1 hour"
                        )
        except Exception as e:
            return f"❌ Error parsing reminder: {e}"
    
    elif "list reminders" in query or "show reminders" in query:
        return reminder_system.list_active_reminders()
    
    elif "start reminder" in query:
        reminder_system.start_monitoring()
        return "🔔 Reminder system started!"
    
    elif "stop reminder" in query:
        reminder_system.stop_monitoring()
        return "🔔 Reminder system stopped!"
    
    else:
        return """🔔 REMINDER SYSTEM COMMANDS:

📝 Set Reminders:
• "set reminder to call mom at 3:00"
• "remind me to exercise in 2 hours"
• "set reminder to meeting tomorrow at 10:00"

📋 Manage Reminders:
• "list reminders" - Show active reminders
• "start reminder system" - Begin monitoring
• "stop reminder system" - Stop monitoring

⏰ Time Formats:
• "in 30 minutes", "in 2 hours", "in 3 days"
• "at 14:30", "tomorrow at 9:00"
• "now", "immediately"
"""

if __name__ == "__main__":
    # Test the reminder system
    print("🔔 Testing Smart Reminder System...")
    
    # Add test reminders
    result1 = reminder_system.add_reminder("Test Meeting", "Don't forget the team meeting", "in 1 minute")
    print(result1)
    
    result2 = reminder_system.add_reminder("Lunch Break", "Time for lunch!", "in 2 minutes")
    print(result2)
    
    # List reminders
    print("\n" + reminder_system.list_active_reminders())
    
    # Start monitoring
    reminder_system.start_monitoring()
    print("Monitoring started - waiting for reminders...")
    
    # Wait a bit to see if reminders trigger
    time.sleep(65)
    
    reminder_system.stop_monitoring()
    print("✅ Reminder system test complete!")