#!/usr/bin/env python3
"""
NEXUS Modern Main Entry Point
Enhanced main execution with modern GUI integration
"""

import subprocess
import threading
import json
import os
import sys
import re
import queue
from time import sleep
from asyncio import run
from dotenv import dotenv_values
import pygame

# Import both GUI systems
from Interface.GUI import GraphicalUserInterface
from Interface.ModernGUI import ModernGraphicalUserInterface
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import prepare_speech_engine, capture_speech
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.WebDriverService import get_webdriver_service
from Backend.InterruptService import is_interrupted
from Backend.FileReader import get_text_from_pdf, summarize_text
from Backend.Agents.StockAgent import StockAgent
from Backend.Agents.DSAAgent import DSAAgent
from Backend.Agents.DSASetup import setup_dsa_usernames
from Backend.ModeManager import switch_mode, get_mode_info, should_route_to_mode, get_current_mode
from Backend.Agents.ProjectAgent import ProjectAgent, start_project_reminders, get_project_exit_warning
from Backend.SharedServices import gui_queue, backend_queue
from personal_assistant_manager import PersonalAssistantManager

# --- CONFIGURATION ---
def setup_environment():
    env_path = ".env"
    env_vars = dotenv_values(env_path)
    for key, value in env_vars.items():
        os.environ[key] = value
    return env_vars

env_vars = setup_environment()
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search", "mail"]
subprocesses = []

# --- HELPERS ---
def update_gui(msg_type, data=None):
    gui_queue.put({"type": msg_type, "data": data})

def sanitize_for_speech(text):
    if not text:
        return ""
    # Remove markdown-style formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\\1', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'\\1', text)      # Italic
    text = re.sub(r'`(.*?)`', r'\\1', text)        # Code
    text = re.sub(r'#{1,6}\s*(.*)', r'\\1', text)  # Headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\\1', text) # Links
    text = re.sub(r'[•·▪▫◦‣⁃]', '-', text)        # Bullet points
    text = re.sub(r'[\r\n]+', ' ', text)           # Line breaks
    text = re.sub(r'\s+', ' ', text)               # Multiple spaces
    return text.strip()

# Enhanced chat history management
chat_history = []

def add_to_chat_history(user_message, assistant_response):
    timestamp = f"{len(chat_history) + 1:03d}"
    chat_history.append({
        "timestamp": timestamp,
        "user": user_message,
        "assistant": assistant_response
    })

def get_formatted_chat_history():
    if not chat_history:
        return """
        <div style="padding: 20px; text-align: center; color: #888;">
            <h3>Welcome to NEXUS Complete Personal Assistant! 🚀</h3>
            <p>Your comprehensive AI companion for career growth and daily life management.</p>
            <div style="margin: 20px 0; padding: 15px; background: rgba(108, 99, 255, 0.1); border-radius: 10px;">
                <strong>✨ What I can help you with:</strong><br>
                🏢 Career acceleration & interview prep<br>
                📚 DSA learning & coding practice<br>
                🚀 Project management & development<br>
                📈 Stock analysis & market insights<br>
                🏠 Complete personal life management<br>
                📱 WhatsApp integration for mobile access
            </div>
            <p style="color: #6C63FF;"><strong>Try saying: "show my calendar" or "help me prepare for interviews"</strong></p>
        </div>
        """
    
    html = ""
    for entry in chat_history:
        html += f"""
        <div style="margin-bottom: 25px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.02);">
            <div style="color: #6C63FF; font-weight: bold; margin-bottom: 8px;">
                [{entry['timestamp']}] You:
            </div>
            <div style="color: #E0E0E0; margin-bottom: 15px; padding-left: 10px; border-left: 3px solid #6C63FF;">
                {entry['user']}
            </div>
            <div style="color: #00D4AA; font-weight: bold; margin-bottom: 8px;">
                NEXUS:
            </div>
            <div style="color: #F0F0F0; padding-left: 10px; border-left: 3px solid #00D4AA; line-height: 1.6;">
                {entry['assistant']}
            </div>
        </div>
        """
    return html

def reset_chat_log():
    global chat_history
    chat_history = []

# --- ENHANCED QUERY PROCESSING ---
def ProcessQuery(Query):
    print(f"🔍 Processing Query: '{Query}'")
    Decision = FirstLayerDMM(Query)
    print(f"Decision : {Decision}")
    
    TaskExecution = False
    ImageExecution = False
    Answer = ""

    # Handle image generation
    image_queries = [q for q in Decision if q.startswith("generate")]
    if image_queries:
        ImageExecution = True
        prompt = " ".join([q.replace("generate ", "") for q in image_queries])
        update_gui("status", f"🎨 Generating images for: '{prompt}'...")
        try:
            p = subprocess.Popen([sys.executable, r'Backend\\ImageGeneration.py', prompt])
            subprocesses.append(p)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")
            Answer = f"❌ Image generation failed: {e}"

    # Check for project commands first (higher priority)
    is_project_cmd = any(d.startswith("project") for d in Decision)
    
    # Handle automation
    automation_queries = [q for q in Decision if any(q.startswith(func) for func in Functions)]
    if automation_queries and not is_project_cmd:
        TaskExecution = True
        run(Automation(automation_queries))

    if not TaskExecution and not ImageExecution:
        # Enhanced query classification
        mode_type, mode_query = should_route_to_mode(Query, Decision)
        
        # Enhanced keyword detection
        dsa_keywords = ['arrays guide', 'trees guide', 'strings guide', 'graphs guide', 'dynamic programming guide', 'dp guide', 'dsa guide', 'prep guide', 'study guide']
        is_dsa_guide = any(keyword in Query.lower() for keyword in dsa_keywords)
        
        project_switch_keywords = ['switch to project', 'select project', 'change to project', 'switch to nexus', 'switch to testrepo', 'switch to mynewapp', 'switch to testapp', 'switch to']
        is_project_switch = any(keyword in Query.lower() for keyword in project_switch_keywords)
        
        git_keywords = ['save', 'push', 'pull', 'sync', 'git status', 'git add', 'git commit', 'git push', 'git pull', 'git init', 'git clone', 'git branch']
        is_git_command = any(keyword in Query.lower() for keyword in git_keywords) and mode_type == "project"
        
        # NEXUS career acceleration commands
        nexus_keywords = [
            'nexus', 'career', 'company research', 'build resume', 'optimize resume', 
            'start assessment', 'start interview', 'mock interview', 'practice interview',
            'career progress', 'interview simulation', 'behavioral interview', 'technical interview',
            'company intelligence', 'resume building', 'skill assessment', 'interview practice',
            'research google', 'research microsoft', 'research amazon', 'research apple',
            'research netflix', 'research meta', 'research facebook', 'tell me about.*company'
        ]
        
        # Enhanced personal assistant keywords
        personal_assistant_keywords = [
            'schedule', 'calendar', 'appointment', 'meeting', 'task', 'todo', 'expense', 'budget', 
            'health', 'fitness', 'contact', 'bill', 'reminder', 'shopping', 'movie', 'music',
            'entertainment', 'weather', 'news', 'personal assistant', 'show calendar', 'show tasks',
            'show expenses', 'show contacts', 'show bills', 'add task', 'add expense', 'add contact',
            'log health', 'log workout', 'log steps', 'health summary', 'find contact', 'add appointment'
        ]
        
        is_nexus = any(keyword in Query.lower() for keyword in nexus_keywords) or any(d.startswith("nexus") for d in Decision)
        is_personal_assistant = any(keyword in Query.lower() for keyword in personal_assistant_keywords) or any(d.startswith("personal") for d in Decision)
        
        # Determine query type
        is_general = any(d.startswith("general") for d in Decision)
        is_realtime = any(d.startswith("realtime") for d in Decision)
        is_stock = any(d.startswith("stock") for d in Decision)
        is_dsa = any(d.startswith("dsa") for d in Decision) or is_dsa_guide
        is_setup_dsa = any(d.startswith("setup_dsa") for d in Decision)
        is_setup_github = any(d.startswith("setup_github") for d in Decision)
        is_reminder = any(d.startswith("reminder") for d in Decision)
        is_project = any(d.startswith("project") for d in Decision) or is_project_switch or is_git_command
        is_mode = any(d.startswith("mode") for d in Decision)
        
        # Enhanced special handling for misclassified commands
        if is_general and is_project_switch:
            is_general = False
            is_project = True
            print("🔄 Detected misclassified project switch command, routing to ProjectAgent")
        
        if is_general and mode_type == "project" and any(keyword in Query.lower() for keyword in git_keywords):
            is_general = False
            is_project = True
            print("🔄 Detected misclassified git command in project mode, routing to ProjectAgent")
        
        # Mode fallback logic
        if not any([is_general, is_realtime, is_stock, is_dsa, is_setup_dsa, is_setup_github, is_reminder, is_project, is_personal_assistant]):
            if mode_type == "stock":
                is_stock = True
            elif mode_type == "dsa":
                is_dsa = True
            elif mode_type == "project":
                is_project = True
        
        print(f"🧠 Query Analysis: mode={get_current_mode()}, is_stock={is_stock}, is_dsa={is_dsa}, is_project={is_project}, is_personal_assistant={is_personal_assistant}, is_nexus={is_nexus}")
        
        # Enhanced routing logic
        if any([is_nexus, is_general, is_realtime, is_stock, is_dsa, is_setup_dsa, is_setup_github, is_reminder, is_mode, is_project, is_personal_assistant]):
            if is_personal_assistant:
                print(f"🤖 Routing to Personal Assistant: '{Query}'")
                try:
                    pa = PersonalAssistantManager()
                    Answer = pa.process_personal_assistant_query(Query)
                except Exception as e:
                    Answer = f"""🤖 **Personal Assistant**
⚠️ System temporarily unavailable: {str(e)}

🏠 **Available Features:**
• Calendar management
• Task tracking  
• Expense monitoring
• Health logging
• Contact management
• Bill tracking
• Entertainment recommendations

Please try again in a moment!"""
            elif is_nexus:
                print(f"🚀 Routing to NEXUS Career System: '{Query}'")
                try:
                    from Backend.Agents.NEXUSAgent import NEXUS
                    Answer = NEXUS(Query)
                except ImportError:
                    Answer = """🚀 **NEXUS Career Acceleration System**
⚠️ NEXUS system components are being initialized...

Available career acceleration features:
🏢 Company Intelligence & Research
📄 Resume Building & Optimization  
📊 Skill Assessment & Testing
🎬 AI Interview Simulation

To activate NEXUS, ensure all system components are properly installed."""
            elif is_stock:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("stock")])
                print(f"📈 Routing to Stock Agent: '{query}'")
                Answer = StockAgent(query)
            elif is_dsa:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("dsa")])
                print(f"📚 Routing to DSA Agent: '{query}'")
                Answer = DSAAgent(query)
            elif is_project:
                if is_project_switch or is_git_command or mode_type == "project":
                    query = Query
                    print(f"🚀 Routing to Project Agent: '{query}'")
                    Answer = ProjectAgent(query)
                else:
                    query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("project")])
                    print(f"🚀 Routing to Project Agent: '{query}'")
                    Answer = ProjectAgent(query)
            elif is_mode:
                mode_query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("mode")])
                if ("switch to" in mode_query.lower() or mode_query.lower().startswith("project ")) and len(mode_query.split()) > 1:
                    print(f"🚀 Routing mode switch to Project Agent: '{mode_query}'")
                    Answer = ProjectAgent(mode_query)
                elif "stock" in mode_query.lower() and mode_query.lower().strip() == "stock":
                    Answer = switch_mode("stock")
                elif "dsa" in mode_query.lower() and mode_query.lower().strip() == "dsa":
                    Answer = switch_mode("dsa")
                elif "project" in mode_query.lower() and mode_query.lower().strip() == "project":
                    Answer = switch_mode("project")
                elif "general" in mode_query.lower() or "normal" in mode_query.lower():
                    if get_current_mode() == "project":
                        warnings = get_project_exit_warning()
                        if warnings:
                            Answer = warnings[0]
                        else:
                            Answer = switch_mode("general")
                    else:
                        Answer = switch_mode("general")
                else:
                    Answer = get_mode_info()
            elif is_setup_github:
                print("🔧 Running GitHub setup...")
                from Backend.Agents.GitHubSetup import setup_github_credentials, verify_github_setup
                if setup_github_credentials():
                    is_valid, message = verify_github_setup()
                    Answer = f"✅ GitHub setup completed!\\n\\n{message}\\n\\nYou can now use Git integration in project mode!"
                else:
                    Answer = "❌ GitHub setup failed. Please try again."
            elif is_setup_dsa:
                print("⚙️ Running DSA setup...")
                Answer = "DSA setup completed! Your platform usernames have been configured."
                setup_dsa_usernames()
            elif is_reminder:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("reminder")])
                print(f"🔔 Routing to Reminder Agent: '{query}'")
                from Backend.smart_reminders import ReminderAgent
                Answer = ReminderAgent(query)
            elif is_realtime:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("realtime")])
                print(f"🌐 Routing to Realtime Search: '{query}'")
                Answer = RealtimeSearchEngine(query)
            else:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("general")])
                print(f"💬 Routing to ChatBot: '{query}'")
                Answer = ChatBot(query or Query)
        else:
            print(f"💬 Defaulting to ChatBot: '{Query}'")
            Answer = ChatBot(Query)

    # Add to chat history
    if Answer:
        add_to_chat_history(Query, Answer)

    # Update GUI
    update_gui("chat", get_formatted_chat_history())
    update_gui("status", "Answering...")
    
    # Enhanced text-to-speech
    try:
        clean_answer = sanitize_for_speech(Answer)
        if clean_answer.strip():
            TextToSpeech(clean_answer)
            if is_interrupted():
                TextToSpeech("Okay.")
    except Exception as e:
        print(f"❌ TTS Error: {e}")
    
    update_gui("status", "Ready")

def handle_pdf_analysis(filepath: str):
    """Enhanced PDF analysis"""
    try:
        update_gui("status", "📄 Reading PDF...")
        text = get_text_from_pdf(filepath)
        update_gui("status", "🧠 Analyzing content...")
        summary = summarize_text(text)
        update_gui("pdf_summary", summary)
        update_gui("status", "✅ Analysis complete")
    except Exception as e:
        update_gui("pdf_summary", f"❌ Error analyzing PDF: {e}")
        update_gui("status", "❌ Analysis failed")

# --- MAIN EXECUTION ---
def main(use_modern_gui=True):
    """Enhanced main execution with GUI selection"""
    print(f"🚀 Starting {Assistantname} Assistant...")
    print(f"🎨 Using {'Modern' if use_modern_gui else 'Classic'} GUI")
    
    # Initialize audio
    pygame.mixer.init()
    try:
        activation_sound = pygame.mixer.Sound(r"Interface\\Graphics\\activate.wav")
    except:
        activation_sound = None
    
    # Initialize project reminders
    start_project_reminders()
    
    # Enhanced backend loop
    def enhanced_backend_loop():
        print("🔄 Starting enhanced backend loop...")
        while True:
            try:
                if not backend_queue.empty():
                    message = backend_queue.get_nowait()
                    msg_type = message.get("type")
                    data = message.get("data")
                    
                    if msg_type == "text_query":
                        ProcessQuery(data)
                    elif msg_type == "reset_chat":
                        reset_chat_log()
                        update_gui("chat", get_formatted_chat_history())
                    elif msg_type == "analyze_pdf":
                        handle_pdf_analysis(data)
                    elif msg_type == "activate_voice":
                        # Voice activation logic would go here
                        update_gui("status", "🎤 Voice activation requested...")
                        
                sleep(0.1)  # Prevent excessive CPU usage
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Backend loop error: {e}")
                continue
    
    # Start backend thread
    backend_thread = threading.Thread(target=enhanced_backend_loop, daemon=True)
    backend_thread.start()
    
    # Launch GUI
    try:
        if use_modern_gui:
            print("🎨 Launching Modern GUI...")
            ModernGraphicalUserInterface()
        else:
            print("🎨 Launching Classic GUI...")
            GraphicalUserInterface()
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        print("🔄 Falling back to Classic GUI...")
        GraphicalUserInterface()

if __name__ == "__main__":
    # Check command line arguments for GUI selection
    use_modern = "--modern" in sys.argv or "--new" in sys.argv
    use_classic = "--classic" in sys.argv or "--old" in sys.argv
    
    if use_classic:
        main(use_modern_gui=False)
    else:
        main(use_modern_gui=True)  # Default to modern GUI