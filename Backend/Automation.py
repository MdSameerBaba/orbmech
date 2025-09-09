# In Backend/Automation.py

# --- IMPORTS ---
import webbrowser
import subprocess
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AppOpener import close, open as appopen
from pywhatkit import search as pywhatkit_search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from groq import Groq
import requests
import keyboard

# --- IMPROVEMENT: Resilient Import for Emailer ---
try:
    from Backend.Emailer import send_email
    EMAIL_FEATURE_ENABLED = True
except ImportError:
    print("⚠️ Warning: Could not import Emailer.py. The 'mail' feature will be disabled.")
    send_email = None
    EMAIL_FEATURE_ENABLED = False
# --- END IMPROVEMENT ---

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in Automation module: {e}"); client = None

requests_session = requests.Session()
requests_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

def ContentWriterAI(prompt: str):
    if not client: return "Content writer AI is not available."
    # --- GLITCH FIX: Restored full system prompt ---
    system_prompt = f"You are a professional content writer. The user's name is {Username}. Write content in a professional and clear manner based on the user's request."
    # --- END GLITCH FIX ---
    messages_to_send = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages_to_send, max_tokens=3072, temperature=0.7, stream=True)
        Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
        return Answer.strip().replace("</s>", "")
    except Exception as e:
        print(f"❌ Error in ContentWriterAI: {e}"); return f"Sorry, I was unable to generate content due to an error: {e}"

def GoogleSearch(topic: str):
    try:
        print(f"🔍 Searching Google for: '{topic}'"); pywhatkit_search(topic); return True
    except Exception as e: print(f"❌ Error during Google search for '{topic}': {e}"); return False

def Content(topic: str):
    try:
        print(f"✍️ Generating content for: '{topic}'"); content_by_ai = ContentWriterAI(topic)
        safe_filename = "".join(c for c in topic if c.isalnum() or c in " _-").rstrip()[:50]
        filepath = os.path.join("Data", f"{safe_filename}.txt")
        with open(filepath, "w", encoding="utf-8") as f: f.write(content_by_ai)
        subprocess.Popen(['notepad.exe', filepath]); return True
    except Exception as e: print(f"❌ Error in Content task for '{topic}': {e}"); return False

def YoutubeSearch(topic: str):
    try:
        print(f"📺 Searching YouTube for: '{topic}'"); url = f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"
        webbrowser.open(url); return True
    except Exception as e: print(f"❌ Error during YouTube search for '{topic}': {e}"); return False

def PlayOnYoutube(query: str):
    try:
        print(f"▶️ Playing on YouTube: '{query}'"); playonyt(query); return True
    except Exception as e: print(f"❌ Error playing '{query}' on YouTube: {e}"); return False

def OpenApp(app_name: str):
    try:
        print(f"💻 Opening application: '{app_name}'"); appopen(app_name, match_closest=True, output=False, throw_error=True); return True
    except Exception:
        print(f"🌐 App not found. Searching for website: '{app_name}'")
        try:
            response = requests_session.get(f"https://www.google.com/search?q={app_name}")
            response.raise_for_status(); soup = BeautifulSoup(response.text, 'html.parser')
            link_tag = soup.find('div', class_='egMi0 kCrYT')
            if link_tag and (a_tag := link_tag.find('a')):
                link = a_tag.get('href')
                if link.startswith('/url?q='): webbrowser.open(link.split('/url?q=')[1].split('&sa=U')[0]); return True
            webbrowser.open(f"https://www.google.com/search?q={app_name}"); return True
        except Exception as e: print(f"❌ Error opening website '{app_name}': {e}"); return False

def CloseApp(app_name: str):
    try:
        print(f"🛑 Closing application: '{app_name}'"); close(app_name, match_closest=True, output=False, throw_error=True); return True
    except Exception as e: print(f"❌ Error closing application '{app_name}': {e}"); return False

def System(command: str):
    try:
        print(f"🔊 Executing system command: '{command}'")
        actions = {"mute": "volume mute", "unmute": "volume unmute", "volume up": "volume up", "volume down": "volume down"}
        if command in actions: keyboard.press_and_release(actions[command]); return True
        else: print(f"⚠️ Unknown system command: '{command}'"); return False
    except Exception as e: print(f"❌ Error with system command '{command}': {e}"); return False

async def Automation(commands: list[str]):
    command_map = {
        "open": OpenApp, "close": CloseApp, "play": PlayOnYoutube, "content": Content,
        "google search": GoogleSearch, "youtube search": YoutubeSearch, "system": System,
    }
    if EMAIL_FEATURE_ENABLED: command_map["mail"] = send_email

    tasks = []
    for command in commands:
        try:
            command_type, argument = command.split(" ", 1)
            if command_type == "mail" and EMAIL_FEATURE_ENABLED:
                if " about " in argument:
                    recipient, mail_content = argument.split(" about ", 1)
                    self_synonyms = ["yourself", "me", "my self"]
                    if recipient.strip().lower() in self_synonyms: recipient = "myself"
                    tasks.append(asyncio.to_thread(command_map[command_type], recipient, mail_content))
                else: print(f"⚠️ Malformed mail command, missing 'about': '{command}'")
            elif command_type in command_map:
                tasks.append(asyncio.to_thread(command_map[command_type], argument))
            else: print(f"⚠️ No automation function found for command: '{command}'")
        except ValueError: print(f"⚠️ Malformed command, cannot execute: '{command}'")
    
    if tasks:
        print(f"🚀 Running {len(tasks)} automation task(s) concurrently...")
        await asyncio.gather(*tasks, return_exceptions=True)
    print("✅ Automation sequence complete.")
    return True

if __name__ == "__main__":
    if EMAIL_FEATURE_ENABLED:
        test_commands = ["mail myself about this is a test email from the automation script"]
        asyncio.run(Automation(test_commands))