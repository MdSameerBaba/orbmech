# In Backend/Chatbot.py

# --- IMPORTS ---
import json
import datetime
from dotenv import dotenv_values
from groq import Groq

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client: {e}"); client = None

# --- CONSTANTS ---
CHATLOG_FILE = r"Data\Chatlog.json"
CONTEXT_WINDOW_MESSAGES = 30 # For sliding window

# --- HELPER FUNCTIONS (unchanged) ---
def get_system_prompt():
    return f"""You are Nexus, a highly advanced AI assistant for a user named {Username}.
Your primary goal is to be accurate and helpful, but your personality is defined by your sharp wit and a dry, clever sense of humor.
**Your Personality Guidelines:**
- Be Witty, Not Goofy: Your humor should be intelligent...
- Inject Personality...
- Sarcasm is a Tool...
- Be Conversational...
- Stay Helpful...
"""
def get_realtime_information():
    now = datetime.datetime.now()
    return f"Current real-time information:\n- Day: {now.strftime('%A')}..."

def read_chat_history():
    try:
        with open(CHATLOG_FILE, "r", encoding='utf-8') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return []
def write_chat_history(history: list):
    try:
        with open(CHATLOG_FILE, "w", encoding='utf-8') as f: json.dump(history, f, indent=4)
    except IOError as e: print(f"❌ Error writing to chat log: {e}")

# --- REWRITTEN CORE CHATBOT LOGIC ---
def ChatBot(Query: str):
    """
    Handles a conversational query. This function is now completely stateless,
    ensuring it always reads the latest chat history from the disk.
    """
    if not client: return "I'm sorry, my connection to the AI model is not configured correctly."
    if not Query: return "It seems you didn't say anything. How can I help?"

    # --- THE FIX: ALWAYS READ THE LATEST HISTORY ---
    # We no longer rely on a global 'messages' list. We read from the file every time.
    full_history = read_chat_history()
    full_history.append({"role": "user", "content": Query})

    # Sliding window for context
    recent_history = full_history[-CONTEXT_WINDOW_MESSAGES:]

    messages_to_send = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "system", "content": get_realtime_information()}
    ] + recent_history

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages_to_send,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.strip().replace("</s>", "")

        # Append the new response to our full history list
        full_history.append({"role": "assistant", "content": Answer})
        # Write the complete, updated history back to the file
        write_chat_history(full_history)
        
        return Answer

    except Exception as e:
        print(f"❌ Error during Groq API call in ChatBot: {e}")
        # Non-destructive error handling: remove the failed query
        full_history.pop()
        write_chat_history(full_history)
        return "I'm sorry, I encountered an error while processing your request. Please try again."


# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("ChatBot module test. Type 'exit' to end.")
    while True:
        user_input = input(f"{Username}: ")
        if user_input.lower() == 'exit':
            break
        response = ChatBot(user_input)
        print(f"{Assistantname}: {response}")