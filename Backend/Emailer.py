# In Backend/Emailer.py

# --- IMPORTS ---
import smtplib
import json
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values

# --- PROJECT PATH FIX ---
# This ensures that imports from other backend modules work reliably.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- REVISED IMPORT ---
# Now uses an absolute path for maximum reliability.
try:
    from Backend.Automation import ContentWriterAI
except ImportError:
    # This fallback is now more robust and will only be used if Automation.py is missing.
    print("⚠️ Warning: Could not import ContentWriterAI from Automation.py. Using local fallback.")
    from groq import Groq
    env_vars_local = dotenv_values(".env")
    client = Groq(api_key=env_vars_local.get("GroqAPIKey"))
    def ContentWriterAI(prompt: str):
        completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}], stream=False)
        return completion.choices[0].message.content
# --- END REVISED IMPORT ---

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
SENDER_EMAIL = env_vars.get("MyEmail").strip('"') if env_vars.get("MyEmail") else None
SENDER_PASSWORD = env_vars.get("EmailAppPassword").strip('"') if env_vars.get("EmailAppPassword") else None
CONTACTS_FILE = r"Data\contacts.json"

print(f"Debug: SENDER_EMAIL = {SENDER_EMAIL}")
print(f"Debug: SENDER_PASSWORD = {'*' * len(SENDER_PASSWORD) if SENDER_PASSWORD else 'None'}")

# --- HELPER FUNCTIONS ---
def get_contact_email(name: str):
    """Finds the email address for a given name from the contacts file."""
    try:
        with open(CONTACTS_FILE, 'r') as f: data = json.load(f); return data["contacts"].get(name.lower())
    except (FileNotFoundError, json.JSONDecodeError): return None

def draft_email(prompt: str):
    """Uses an LLM to draft a professional email subject and body."""
    print("🤖 Drafting email...")
    drafting_prompt = f"""
    You are an AI assistant tasked with writing a professional email. Based on the following user request, generate a suitable subject line and a well-formatted email body.
    User Request: "{prompt}"
    Respond in the following format ONLY:
    Subject: [Your generated subject line]
    ---
    [Your generated email body]
    """
    draft = ContentWriterAI(drafting_prompt)
    try:
        subject_part, body_part = draft.split("---", 1)
        subject = subject_part.replace("Subject:", "").strip(); body = body_part.strip()
        return subject, body
    except ValueError:
        print("⚠️ AI did not follow formatting. Using fallback."); return "Regarding Your Request", draft

# --- CORE EMAIL SENDING LOGIC ---
def send_email(recipient_name: str, email_prompt: str):
    """Finds the recipient, drafts an email, and sends it via Gmail's SMTP server."""
    print(f"📧 Initiating email to '{recipient_name}'...")
    recipient_email = get_contact_email(recipient_name)
    if not recipient_email:
        error_msg = f"Sorry, I could not find a contact named '{recipient_name}' in your contact list."
        print(f"❌ {error_msg}"); return error_msg

    subject, body = draft_email(email_prompt)
    message = MIMEMultipart(); message["From"] = SENDER_EMAIL; message["To"] = recipient_email
    message["Subject"] = subject; message.attach(MIMEText(body, "plain"))

    try:
        print(f"📬 Connecting to Gmail SMTP server...")
        print(f"Debug: Sending from {SENDER_EMAIL} to {recipient_email}")
        print(f"Debug: Subject: {subject}")
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)  # Enable SMTP debugging
            server.starttls()
            print("Debug: Attempting login...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Debug: Login successful, sending email...")
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
            print(f"✅ Email sent successfully to {recipient_name} ({recipient_email})!")
        success_msg = f"Alright, I have sent the email to {recipient_name}."
        return success_msg
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"Authentication failed: {e}. Check your email and app password."
        print(f"❌ {error_msg}"); return error_msg
    except Exception as e:
        error_msg = f"Email sending failed: {e}"
        print(f"❌ {error_msg}"); return error_msg

# --- TESTING BLOCK ---
if __name__ == "__main__":
    recipient = "myself"
    prompt = "remind me to check the project status by end of day"
    result = send_email(recipient_name=recipient, email_prompt=prompt)
    print(f"\nFinal Result: {result}")