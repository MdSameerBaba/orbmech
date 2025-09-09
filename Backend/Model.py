# In Backend/Model.py

# --- IMPORTS ---
from dotenv import dotenv_values
from groq import Groq

# --- CONFIGURATION ---
env_vars= dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in Model.py: {e}"); client = None

funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate",
    "system", "content", "google search", "youtube search", "remainder", "mail", "stock", "dsa", "setup_dsa", "mode", "project", "setup_github"
]
  
# --- IMPROVEMENT: A slightly more robust preamble ---
preamble = """
You are an ultra-fast, accurate classification model. Your single purpose is to parse a user's query and output one or more predefined function calls.
Do not be conversational. Do not explain yourself. Your output must STRICTLY follow the specified format.

RULES:
1. Classify the user's query into one or more of the following function calls:
   - 'general (query)': For conversation, simple questions, or if unsure.
   - 'realtime (query)': For news, weather, current events, or facts about public figures/companies.
   - 'open (app/website)': To open applications or websites.
   - 'close (app/website)': To close applications.
   - 'play (song name)': To play a song.
   - 'generate (image prompt)': To create an image.
   - 'mail (recipient) about (content)': To send an email. The word 'about' MUST be present.
   - 'system (task)': For system commands like 'volume up', 'mute'.
   - 'content (topic)': To write text, code, or other content.
   - 'google search (topic)': To perform a Google search.
   - 'youtube search (topic)': To search on YouTube.
   - 'stock (query)': For portfolio analysis, stock prices, or investment questions.
   - 'dsa (query)': For coding problems, algorithm practice, LeetCode, CodeChef, Codeforces, HackerRank progress, DSA guides, prep guides, study plans, arrays guide, trees guide, etc.
   - 'setup_dsa': To configure DSA platform usernames for tracking.
   - 'project (query)': For project management, tracking progress, creating projects, deadlines, work logging, project dashboard.
   - 'setup_github': To configure GitHub credentials and authentication for Git integration.
   - 'mode (mode_name)': To switch between different assistant modes (general, stock, dsa, project).
   - 'exit': If the user indicates they want to end the conversation.

2. If the query requires multiple actions, separate the function calls with a comma.
   EXAMPLE: "open chrome and tell me a joke" -> "open chrome, general tell me a joke"
   EXAMPLE: "email john about the meeting and play some music" -> "mail john about the meeting, play some music"
"""
# --- END IMPROVEMENT ---

ChatHistory = [
    {"role": "user", "content": "how are you?"},
    {"role": "assistant", "content": "general how are you?"},
    {"role": "user", "content": "open chrome and tell me about mahatma gandhi."},
    {"role": "assistant", "content": "open chrome, realtime tell me about mahatma gandhi."},
    {"role": "user", "content": "open chrome and firefox"},
    {"role": "assistant", "content": "open chrome, open firefox"},
    {"role": "user", "content": "email maria that the project is complete"},
    {"role": "assistant", "content": "mail maria about the project is complete"},
    {"role": "user", "content": "arrays guide"},
    {"role": "assistant", "content": "dsa arrays guide"},
    {"role": "user", "content": "bye nexus"},
    {"role": "assistant", "content": "exit"}
]

def FirstLayerDMM(prompt: str = "test", max_retries: int = 2):
    """Uses Groq's LLaMA3-8B for ultra-fast decision making."""
    if not client: return ["general " + prompt]

    messages_to_send = [{"role": "system", "content": preamble}] + ChatHistory + [{"role": "user", "content": prompt}]

    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", messages=messages_to_send,
                temperature=0.0, max_tokens=150, stream=False
            )
            response_text = completion.choices[0].message.content.replace("\n", "").strip()
            tasks = [task.strip() for task in response_text.split(',')]
            validated_tasks = [task for task in tasks if any(task.startswith(func) for func in funcs)]
            if validated_tasks: return validated_tasks
            print(f"⚠️ DMM validation failed on attempt {attempt+1}. Response: '{response_text}'")
        except Exception as e:
            print(f"❌ Error during Groq DMM call on attempt {attempt+1}: {e}")

    print("⚠️ DMM failed after all retries. Defaulting to 'general' query.")
    return ["general " + prompt]

if __name__ == "__main__":
    while True: print(FirstLayerDMM(input(">>> ")))