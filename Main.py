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
# NOTE: Use two queues: gui_queue for backend->GUI, backend_queue for GUI->backend
from Backend.SharedServices import gui_queue, backend_queue
# --- CONFIGURATION ---
def setup_environment():
    env_path = ".env"; env_vars = dotenv_values(env_path)
    for key, value in env_vars.items(): os.environ[key] = value
    return env_vars

env_vars = setup_environment()
Username = env_vars.get("Username"); Assistantname = env_vars.get("Assistantname")
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search", "mail"]
# --- REMOVED: gui_queue = queue.Queue() ---
subprocesses = []

# --- HELPERS ---
def update_gui(msg_type, data=None): gui_queue.put({"type": msg_type, "data": data})

def get_formatted_chat_history():
    try:
        with open(r'Data\Chatlog.json', 'r', encoding='utf-8') as file: chat_log = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError): chat_log = []
    if not chat_log: return f"<div style='text-align: center; color:#AAAAAA;'>Welcome {Username}. How may I help you?</div>"
    html = ""
    for entry in chat_log:
        role = entry.get("role"); content = entry.get("content", "").replace('\n', '<br>')
        if role == "user": html += f"""<div style='text-align: right; margin-bottom: 15px;'><div style='display: inline-block; text-align: left; padding: 10px; background-color: #005C4B; color: #FFFFFF; border-radius: 10px; max-width: 70%;'><b>{Username}:</b><br>{content}</div></div>"""
        elif role == "assistant": html += f"""<div style='text-align: left; margin-bottom: 15px;'><div style='display: inline-block; text-align: left; padding: 10px; background-color: #333333; color: #FFFFFF; border-radius: 10px; max-width: 70%;'><b>{Assistantname}:</b><br>{content}</div></div>"""
    return html

def reset_chat_log():
    print("🔄 Resetting chat history.");
    try:
        with open(r'Data\Chatlog.json', 'w') as f: json.dump([], f)
    except IOError as e: print(f"❌ Error resetting chat log: {e}")

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
    Decision = FirstLayerDMM(Query); print(f"Decision : {Decision}")
    TaskExecution, ImageExecution = False, False

    image_queries = [q for q in Decision if q.startswith("generate")]
    if image_queries:
        ImageExecution = True; prompt = " ".join([q.replace("generate ", "") for q in image_queries])
        update_gui("status", f"🎨 Generating images for: '{prompt}'...")
        try: p = subprocess.Popen([sys.executable, r'Backend\ImageGeneration.py', prompt]); subprocesses.append(p)
        except Exception as e: print(f"Error starting ImageGeneration.py: {e}")

    # Check for project commands first (higher priority)
    is_project_cmd = any(d.startswith("project") for d in Decision)
    
    automation_queries = [q for q in Decision if any(q.startswith(func) for func in Functions)]
    if automation_queries and not is_project_cmd: TaskExecution = True; run(Automation(automation_queries))

    if not TaskExecution and not ImageExecution:
        # Check for mode switching
        is_mode = any(d.startswith("mode") for d in Decision)
        
        # Check current mode and route accordingly
        mode_type, mode_query = should_route_to_mode(Query, Decision)
        
        # Check for DSA guide requests that might be misclassified as content
        dsa_keywords = ['arrays guide', 'trees guide', 'strings guide', 'graphs guide', 'dynamic programming guide', 'dp guide', 'dsa guide', 'prep guide', 'study guide']
        is_dsa_guide = any(keyword in Query.lower() for keyword in dsa_keywords)
        
        is_general = any(d.startswith("general") for d in Decision); is_realtime = any(d.startswith("realtime") for d in Decision); is_stock = any(d.startswith("stock") for d in Decision) or mode_type == "stock"; is_dsa = any(d.startswith("dsa") for d in Decision) or is_dsa_guide or mode_type == "dsa"; is_setup_dsa = any(d.startswith("setup_dsa") for d in Decision); is_setup_github = any(d.startswith("setup_github") for d in Decision); is_project = any(d.startswith("project") for d in Decision) or mode_type == "project"
        print(f"Debug: mode={get_current_mode()}, is_stock={is_stock}, is_dsa={is_dsa}, is_project={is_project}, is_setup_dsa={is_setup_dsa}, is_setup_github={is_setup_github}, is_mode={is_mode}, is_general={is_general}, is_realtime={is_realtime}")
        if is_general or is_realtime or is_stock or is_dsa or is_setup_dsa or is_setup_github or is_mode or is_project:
            if is_stock:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("stock")])
                print(f"📈 Calling StockAgent with query: '{query}'")
                Answer = StockAgent(query)
            elif is_mode:
                mode_query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("mode")])
                if "stock" in mode_query.lower():
                    Answer = switch_mode("stock")
                elif "dsa" in mode_query.lower():
                    Answer = switch_mode("dsa")
                elif "project" in mode_query.lower():
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
                if mode_type == "project":
                    query = Query  # Use original query in project mode
                else:
                    query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("project")])
                print(f"📈 Calling ProjectAgent with query: '{query}'")
                Answer = ProjectAgent(query)
                print(f"📈 ProjectAgent Response: {Answer[:200]}...")  # Debug: Show first 200 chars
                
                # Save to chat history
                try:
                    with open(r'Data\Chatlog.json', 'r', encoding='utf-8') as f:
                        chat_log = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    chat_log = []
                
                chat_log.append({"role": "user", "content": Query})
                chat_log.append({"role": "assistant", "content": Answer})
                
                try:
                    with open(r'Data\Chatlog.json', 'w', encoding='utf-8') as f:
                        json.dump(chat_log, f, indent=4)
                except IOError as e:
                    print(f"❌ Error saving chat log: {e}")
            elif is_dsa:
                if is_dsa_guide:
                    query = Query  # Use original query for guide requests
                else:
                    query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith("dsa")])
                print(f"🧠 Calling DSAAgent with query: '{query}'")
                Answer = DSAAgent(query)
            else:
                query = " ".join([" ".join(i.split()[1:]) for i in Decision if i.startswith(("general", "realtime"))])
                Answer = RealtimeSearchEngine(query) if is_realtime else ChatBot(query)
            update_gui("status", "Answering...")
            speech_text = sanitize_for_speech(Answer)
            TextToSpeech(speech_text)
            if is_interrupted(): TextToSpeech("Okay.")
        elif any("exit" in d for d in Decision):
            TextToSpeech("Goodbye."); update_gui("exit"); return False
    
    update_gui("chat", get_formatted_chat_history())
    return True

def handle_pdf_analysis(filepath: str):
    """Worker function to process PDFs with detailed status updates."""
    try:
        # --- STEP 1: TEXT EXTRACTION ---
        print(f"1/3: Starting PDF text extraction for: {filepath}")
        update_gui("status", "Step 1/3: Reading PDF document...")
        pdf_text = get_text_from_pdf(filepath)
        
        # Check if extraction was successful
        if pdf_text.startswith("Error:"):
            print(f"❌ PDF Extraction Failed. Aborting.")
            update_gui("status", "Error: Could not read PDF.")
            update_gui("pdf_summary", f"<p style='color:red;'>{pdf_text}</p>")
            return

        print(f"2/3: PDF text extracted successfully. Submitting for summarization...")
        update_gui("status", "Step 2/3: Summarizing with AI...")
        
        # --- STEP 2: AI SUMMARIZATION ---
        summary = summarize_text(pdf_text)
        
        # Check if summarization was successful
        if summary.startswith("Error:"):
            print(f"❌ AI Summarization Failed. Aborting.")
            update_gui("status", "Error: AI failed to summarize.")
            update_gui("pdf_summary", f"<p style='color:red;'>{summary}</p>")
            return

        print("3/3: Summary received. Formatting for display.")
        update_gui("status", "Step 3/3: Formatting summary...")
        
        # --- STEP 3: FORMATTING AND DISPLAY ---
        summary_html = f"<p>{summary.replace('\n', '<br>')}</p>"
        update_gui("pdf_summary", summary_html)
        update_gui("status", "Analysis Complete.")

    except Exception as e:
        # A final catch-all for any other unexpected errors
        print(f"❌ An unexpected critical error occurred during PDF analysis: {e}")
        update_gui("status", "A critical error occurred.")
        update_gui("pdf_summary", f"<p style='color:red;'>A critical error occurred during the analysis process.</p>")


# --- REVISED MAIN BACKEND THREAD ---

def BackendThread(activation_sound):
    """Handles commands from the GUI queue and voice input."""
    update_gui("chat", get_formatted_chat_history())
    
    while True:
        command_processed = False
        try:
            # <-- CONSUME from backend_queue (GUI -> backend)
            message = backend_queue.get_nowait()
            msg_type = message.get("type")
            
            if msg_type == "text_query":
                ProcessQuery(message.get("data")); command_processed = True
            elif msg_type == "reset_chat":
                reset_chat_log(); update_gui("chat", get_formatted_chat_history()); command_processed = True
            elif msg_type == "analyze_pdf":
                print("✅ BackendThread: Received 'analyze_pdf' command from queue.")
                analysis_thread = threading.Thread(target=handle_pdf_analysis, args=(message.get("data"),), daemon=True)
                analysis_thread.start(); command_processed = True
        except queue.Empty:
            pass

        if not command_processed and GetMicrophoneStatus() == "True":
            SetMicrophoneStatus("False")
            update_gui("status", "Preparing Mic...")
            driver_instance = prepare_speech_engine()
            if driver_instance:
                if activation_sound: activation_sound.play()
                update_gui("status", "Listening...")
                query = capture_speech(driver_instance)
                if query and "issue with" not in query and "didn't hear anything" not in query:
                    ProcessQuery(query)
        
        update_gui("status", "Available...")
        sleep(0.1)

# --- REVISED ENTRY POINT ---
if __name__ == "__main__":
    for key, value in env_vars.items(): os.environ[key] = value
    try:
        get_webdriver_service()
    except Exception:
        print("Could not start WebDriver, STT will not be available. Exiting.")
        sys.exit(1)
        
    print("🔊 Initializing audio mixer...")
    pygame.mixer.init()
    
    try:
        activation_sound = pygame.mixer.Sound(r"interface\Graphics\activate.wav")
    except pygame.error as e:
        print(f"⚠️ Warning: Could not load activation sound: {e}"); activation_sound = None

    # Start project reminder system
    start_project_reminders()
    
    backend_thread = threading.Thread(target=BackendThread, args=(activation_sound,), daemon=True)
    backend_thread.start()
    
    GraphicalUserInterface()
    
    print("🔇 Quitting audio mixer.")
    pygame.mixer.quit()
    
    for p in subprocesses: 
        if p.poll() is None: p.terminate()
    print("Application closed.")
