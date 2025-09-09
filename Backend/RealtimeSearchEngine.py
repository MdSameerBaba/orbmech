
# In Backend/RealtimeSearchEngine.py

# --- IMPORTS ---
import json
import datetime
from dotenv import dotenv_values
from groq import Groq
from googlesearch import search

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
CONTEXT_WINDOW_MESSAGES = 30

# --- HELPER FUNCTIONS ---
def get_system_prompt():
    """Returns the system prompt for the RAG model, maintaining the witty personality."""
    return f"""You are Nexus, a witty and highly intelligent AI assistant for {Username}.
Your task is to answer the user's query by synthesizing the provided Google Search Results.
**Your Execution Guidelines:**
- **Facts are Sacred:** The factual information you provide must come directly from the search results.
- **Deliver with Flair:** While the facts are sacred, your *delivery* should be infused with your signature wit.
- **Synthesize, Don't List:** Weave the information together into a single, coherent, and well-written answer.
- **Acknowledge the Source:** You can playfully mention that you've just scoured the internet.
Your goal is to be as accurate as a news anchor but as entertaining as a talk show host.
"""

def get_realtime_information():
    now = datetime.datetime.now()
    return f"Current real-time information:\n- Day: {now.strftime('%A')}\n- Date: {now.strftime('%d %B %Y')}\n- Time: {now.strftime('%H:%M:%S')}"

def perform_google_search(query: str):
    print(f"🔍 Searching Google for: '{query}'")
    try:
        results = list(search(query, num_results=5, advanced=True))
        if not results: return "No search results found."
        formatted_results = f"Here are the Google Search Results for the query '{query}':\n\n"
        for i, result in enumerate(results):
            formatted_results += f"--- Result {i+1} ---\nTitle: {getattr(result, 'title', 'N/A')}\nDescription: {getattr(result, 'description', 'N/A')}\n\n"
        return formatted_results
    except Exception as e:
        print(f"❌ Google Search failed: {e}"); return None

def read_chat_history():
    try:
        with open(CHATLOG_FILE, "r", encoding='utf-8') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return []

def write_chat_history(history: list):
    try:
        with open(CHATLOG_FILE, "w", encoding='utf-8') as f: json.dump(history, f, indent=4)
    except IOError as e: print(f"❌ Error writing to chat log: {e}")

# --- CORE RAG LOGIC ---
def RealtimeSearchEngine(prompt: str):
    if not client: return "I'm sorry, my connection to the AI model is not configured correctly."
    search_results = perform_google_search(prompt)
    if search_results is None: return "I'm sorry, I'm having trouble connecting to the internet for a search."

    full_history = read_chat_history()
    full_history.append({"role": "user", "content": prompt})
    recent_history = full_history[-CONTEXT_WINDOW_MESSAGES:]

    messages_to_send = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "system", "content": get_realtime_information()},
        {"role": "user", "content": search_results},
    ] + recent_history

    try:
        # --- THE TYPO FIX ---
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", messages=messages_to_send, max_tokens=2048,
            temperature=0.5, top_p=1, stream=True, stop=None
        )
        # --- END FIX ---
        
        Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
        Answer = Answer.strip().replace("</s>", "")
        full_history.append({"role": "assistant", "content": Answer})
        write_chat_history(full_history)
        return Answer
    except Exception as e:
        print(f"❌ Error during Groq API call in RealtimeSearchEngine: {e}")
        full_history.pop(); write_chat_history(full_history)
        return "I'm sorry, I encountered an error while synthesizing the search results."

# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("RealtimeSearchEngine module test. Type 'exit' to end.")
    while True:
        user_input = input(f"{Username}: ");
        if user_input.lower() == 'exit': break
        response = RealtimeSearchEngine(user_input)
        print(f"{Assistantname}: {response}")