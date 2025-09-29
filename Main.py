# In Main.py

# --- IMPORTS ---
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

from Interface.GUI import GraphicalUserInterface, GetMicrophoneStatus, SetMicrophoneStatus
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

def get_formatted_chat_history():
    try:
        with open(r'Data\Chatlog.json', 'r', encoding='utf-8') as file:
            chat_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        chat_log = []
    
    if not chat_log:
        return f"<div style='text-align: center; color:#AAAAAA;'>Welcome {Username}. How may I help you?</div>"
    
    html = ""
    for entry in chat_log:
        role = entry.get("role")
        content = entry.get("content", "").replace('\n', '<br>')
        if role == "user":
            html += f"""<div style='text-align: right; margin-bottom: 15px;'><div style='display: inline-block; text-align: left; padding: 10px; background-color: #005C4B; color: #FFFFFF; border-radius: 10px; max-width: 70%;'><b>{Username}:</b><br>{content}</div></div>"""
        elif role == "assistant":
            html += f"""<div style='text-align: left; margin-bottom: 15px;'><div style='display: inline-block; text-align: left; padding: 10px; background-color: #333333; color: #FFFFFF; border-radius: 10px; max-width: 70%;'><b>{Assistantname}:</b><br>{content}</div></div>"""
    return html

def reset_chat_log():
    print("🔄 Resetting chat history.")
    try:
        with open(r'Data\Chatlog.json', 'w') as f:
            json.dump([], f)
    except IOError as e:
        print(f"❌ Error resetting chat log: {e}")

def sanitize_for_speech(text: str) -> str:
    text = text.replace('*', '').replace('_', '').replace('#', '')
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# --- CORE LOGIC ---
def ProcessQuery(Query: str):
    update_gui("chat", get_formatted_chat_history() + f"""<div style='text-align: right; margin-bottom: 15px;'><div style='display: inline-block; text-align: left; padding: 10px; background-color: #005C4B; color: #FFFFFF; border-radius: 10px; max-width: 70%;'><b>{Username}:</b><br>{Query.replace('\n', '<br>')}</div></div>""")
    update_gui("status", "Thinking...")
    
    Decision = FirstLayerDMM(Query)
    print(f"Decision : {Decision}")
    
    TaskExecution, ImageExecution = False, False
    Answer = ""  # Initialize Answer variable

    # Handle image generation
    image_queries = [q for q in Decision if q.startswith("generate")]
    if image_queries:
        ImageExecution = True
        prompt = " ".join([q.replace("generate ", "") for q in image_queries])
        update_gui("status", f"🎨 Generating images for: '{prompt}'...")
        try:
            p = subprocess.Popen([sys.executable, r'Backend\ImageGeneration.py', prompt])
            subprocesses.append(p)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    # Check for project commands first (higher priority)
    is_project_cmd = any(d.startswith("project") for d in Decision)
    
    # Handle automation
    automation_queries = [q for q in Decision if any(q.startswith(func) for func in Functions)]
    if automation_queries and not is_project_cmd:
        TaskExecution = True
        run(Automation(automation_queries))

    if not TaskExecution and not ImageExecution:
        # Check for mode switching
        is_mode = any(d.startswith("mode") for d in Decision)
        
        # Check current mode and route accordingly
        mode_type, mode_query = should_route_to_mode(Query, Decision)
        
        # Check for DSA guide requests that might be misclassified as content
        dsa_keywords = ['arrays guide', 'trees guide', 'strings guide', 'graphs guide', 'dynamic programming guide', 'dp guide', 'dsa guide', 'prep guide', 'study guide']
        is_dsa_guide = any(keyword in Query.lower() for keyword in dsa_keywords)
        
        # Check for project switching commands that might be misclassified
        project_switch_keywords = ['switch to project', 'select project', 'change to project', 'switch to nexus', 'switch to testrepo', 'switch to mynewapp', 'switch to testapp', 'switch to']
        is_project_switch = any(keyword in Query.lower() for keyword in project_switch_keywords)
        
        # Check for git commands that might be misclassified
        git_keywords = ['save', 'push', 'pull', 'sync', 'git status', 'git add', 'git commit', 'git push', 'git pull', 'git init', 'git clone', 'git branch']
        is_git_command = any(keyword in Query.lower() for keyword in git_keywords) and mode_type == "project"
        
        # Check for NEXUS career acceleration commands
        nexus_keywords = [
            'nexus', 'career', 'company research', 'build resume', 'optimize resume', 
            'start assessment', 'start interview', 'mock interview', 'practice interview',
            'career progress', 'interview simulation', 'behavioral interview', 'technical interview',
            'company intelligence', 'resume building', 'skill assessment', 'interview practice',
            'research google', 'research microsoft', 'research amazon', 'research apple',
            'research netflix', 'research meta', 'research facebook', 'tell me about.*company'
        ]
        is_nexus = any(keyword in Query.lower() for keyword in nexus_keywords) or any(d.startswith("nexus") for d in Decision)
        
        # Determine query type - prioritize explicit decisions over current mode
        is_general = any(d.startswith("general") for d in Decision)
        is_realtime = any(d.startswith("realtime") for d in Decision)
        is_stock = any(d.startswith("stock") for d in Decision)
        is_dsa = any(d.startswith("dsa") for d in Decision) or is_dsa_guide
        is_setup_dsa = any(d.startswith("setup_dsa") for d in Decision)
        is_setup_github = any(d.startswith("setup_github") for d in Decision)
        is_reminder = any(d.startswith("reminder") for d in Decision)
        is_project = any(d.startswith("project") for d in Decision) or is_project_switch or is_git_command
        
        # Special handling for misclassified project switching
        if is_general and is_project_switch:
            is_general = False
            is_project = True
            print("🔄 Detected misclassified project switch command, routing to ProjectAgent")
        
        # Special handling for misclassified git commands when in project mode
        if is_general and mode_type == "project" and any(keyword in Query.lower() for keyword in git_keywords):
            is_general = False
            is_project = True
            print("🔄 Detected misclassified git command in project mode, routing to ProjectAgent")
        
        # Only use mode fallback if no explicit decision was made
        if not any([is_general, is_realtime, is_stock, is_dsa, is_setup_dsa, is_setup_github, is_reminder, is_project]):
            if mode_type == "stock":
                is_stock = True
            elif mode_type == "dsa":
                is_dsa = True
            elif mode_type == "project":
                is_project = True
        
        print(f"Debug: mode={get_current_mode()}, is_stock={is_stock}, is_dsa={is_dsa}, is_project={is_project}, is_setup_dsa={is_setup_dsa}, is_setup_github={is_setup_github}, is_reminder={is_reminder}, is_mode={is_mode}, is_general={is_general}, is_realtime={is_realtime}, is_nexus={is_nexus}")
        
        if is_nexus or is_general or is_realtime or is_stock or is_dsa or is_setup_dsa or is_setup_github or is_reminder or is_mode or is_project:
            if is_nexus:
                print(f"🚀 Calling NEXUS Career Acceleration System with query: '{Query}'")
                try:
                    from Backend.Agents.NEXUSAgent import NEXUS
                    Answer = NEXUS(Query)
                except ImportError:
                    Answer = """
🚀 **NEXUS Career Acceleration System**
⚠️ NEXUS system components are being initialized...

Available career acceleration features:
🏢 Company Intelligence & Research
📄 Resume Building & Optimization  
📊 Skill Assessment & Testing
🎬 AI Interview Simulation

To activate NEXUS, ensure all system components are properly installed.
For now, try specific commands like:
• "DSA practice" for coding challenges
• "Project mode" for development work
• "Stock analysis" for market insights
                    """
            elif is_stock:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("stock")])
                print(f"📈 Calling StockAgent with query: '{query}'")
                Answer = StockAgent(query)
            elif is_mode:
                mode_query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("mode")])
                # Check if it's a project switching command (like "switch to NEXUS Test Project")
                if ("switch to" in mode_query.lower() or mode_query.lower().startswith("project ")) and len(mode_query.split()) > 1:
                    # This is a project switching command, route to ProjectAgent
                    print(f"🚀 Calling ProjectAgent with query: '{mode_query}'")
                    Answer = ProjectAgent(mode_query)
                elif "stock" in mode_query.lower() and mode_query.lower().strip() == "stock":
                    Answer = switch_mode("stock")
                elif "dsa" in mode_query.lower() and mode_query.lower().strip() == "dsa":
                    Answer = switch_mode("dsa")
                elif "project" in mode_query.lower() and mode_query.lower().strip() == "project":
                    Answer = switch_mode("project")
                elif "general" in mode_query.lower() or "normal" in mode_query.lower():
                    # Check for uncommitted changes before leaving project mode
                    if get_current_mode() == "project":
                        warnings = get_project_exit_warning()
                        if warnings:
                            Answer = warnings[0]  # Show first warning
                        else:
                            Answer = switch_mode("general")
                    else:
                        Answer = switch_mode("general")
                elif "info" in mode_query.lower() or not mode_query.strip():
                    Answer = get_mode_info()
                else:
                    Answer = get_mode_info()
            elif is_setup_github:
                print("🔧 Running GitHub setup...")
                from Backend.Agents.GitHubSetup import setup_github_credentials, verify_github_setup
                if setup_github_credentials():
                    is_valid, message = verify_github_setup()
                    Answer = f"✅ GitHub setup completed!\n\n{message}\n\nYou can now use Git integration in project mode!"
                else:
                    Answer = "❌ GitHub setup failed. Please try again."
            elif is_setup_dsa:
                print("⚙️ Running DSA setup...")
                Answer = "DSA setup completed! Your platform usernames have been configured."
                setup_dsa_usernames()
            elif is_project:
                if is_project_switch:
                    # Direct project switching command
                    print(f"🚀 Calling ProjectAgent with query: '{Query}'")
                    Answer = ProjectAgent(Query)
                elif is_git_command:
                    # Direct git command
                    print(f"🚀 Calling ProjectAgent with query: '{Query}'")
                    Answer = ProjectAgent(Query)
                elif mode_type == "project":
                    query = Query  # Use original query in project mode
                    print(f"🚀 Calling ProjectAgent with query: '{query}'")
                    Answer = ProjectAgent(query)
                else:
                    query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("project")])
                    print(f"🚀 Calling ProjectAgent with query: '{query}'")
                    Answer = ProjectAgent(query)
            elif is_reminder:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("reminder")])
                print(f"🔔 Calling ReminderAgent with query: '{query}'")
                from Backend.smart_reminders import ReminderAgent
                Answer = ReminderAgent(query)
            elif is_dsa:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("dsa")])
                print(f"📚 Calling DSAAgent with query: '{query}'")
                Answer = DSAAgent(query)
            elif is_realtime:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("realtime")])
                print(f"🌐 Calling RealtimeSearchEngine with query: '{query}'")
                Answer = RealtimeSearchEngine(query)
            else:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("general")])
                print(f"💬 Calling ChatBot with query: '{query}'")
                Answer = ChatBot(query or Query)
        else:
            print(f"💬 Defaulting to ChatBot for query: '{Query}'")
            Answer = ChatBot(Query)

    # Update GUI with response and set answering status
    update_gui("chat", get_formatted_chat_history())
    update_gui("status", "Answering...")
    
    # Text-to-speech with interrupt service
    try:
        clean_answer = sanitize_for_speech(Answer)
        if clean_answer.strip():
            TextToSpeech(clean_answer)
            # Check for interruption
            if is_interrupted():
                TextToSpeech("Okay.")
    except Exception as e:
        print(f"❌ TTS Error: {e}")
    
    # Set status back to ready
    update_gui("status", "Ready")

def handle_pdf_analysis(filepath: str):
    """Handle PDF analysis in separate thread"""
    try:
        update_gui("status", "Reading PDF...")
        text = get_text_from_pdf(filepath)
        update_gui("status", "Summarizing...")
        summary = summarize_text(text)
        update_gui("pdf_summary", summary)
        update_gui("status", "Analysis complete")
    except Exception as e:
        update_gui("pdf_summary", f"Error analyzing PDF: {e}")
        update_gui("status", "Analysis failed")

# --- MAIN EXECUTION ---
def main():
    print(f"🚀 Starting {Assistantname} Assistant...")
    
    # Initialize audio
    pygame.mixer.init()
    try:
        activation_sound = pygame.mixer.Sound(r"Interface\Graphics\activate.wav")
    except:
        activation_sound = None
    
    # Initialize project reminders
    start_project_reminders()
    
    # Start GUI in main thread to avoid QApplication warning
    # Run backend in separate thread instead
    def backend_loop():
        while True:
            try:
                # Process backend queue messages
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
                        threading.Thread(target=handle_pdf_analysis, args=(data,), daemon=True).start()
                
                # Check for voice input
                if GetMicrophoneStatus() == "True":
                    SetMicrophoneStatus("False")
                    update_gui("status", "Preparing Mic...")
                    
                    try:
                        # Prepare speech engine first (this takes time)
                        driver = prepare_speech_engine()
                        if driver:
                            # Now play activation sound and start listening immediately
                            if activation_sound:
                                activation_sound.play()
                            update_gui("status", "Listening...")
                            
                            speech_text = capture_speech(driver)
                            if speech_text and speech_text.strip():
                                ProcessQuery(speech_text)
                            else:
                                update_gui("status", "No speech detected")
                        else:
                            update_gui("status", "Speech engine not available")
                    except Exception as e:
                        print(f"❌ Speech recognition error: {e}")
                        update_gui("status", "Speech recognition failed")
                
                sleep(0.1)  # Prevent high CPU usage
                
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                break
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                sleep(1)
    
    backend_thread = threading.Thread(target=backend_loop, daemon=True)
    backend_thread.start()
    
    # Start GUI in main thread
    GraphicalUserInterface()
    
    # Cleanup
    pygame.mixer.quit()
    for p in subprocesses:
        if p.poll() is None:
            p.terminate()

if __name__ == "__main__":
    main()