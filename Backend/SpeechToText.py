# In Backend/SpeechToText.py

# --- IMPORTS ---
import os
import sys
import time
import mtranslate as mt
from dotenv import dotenv_values
from selenium.webdriver.common.by import By

# --- PROJECT PATH FIX & ROBUST IMPORT ---
# Ensures that imports from other backend modules work reliably.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Backend.WebDriverService import get_new_driver_instance

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")
SILENCE_TIMEOUT_SECONDS = 1.2

def get_html_code():
    """Generates the HTML code for the speech recognition page."""
    return """
    <!DOCTYPE html><html><head><title>Speech Recognition</title></head>
    <body><p id="output"></p><script>
        const output = document.getElementById('output');
        let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = '""" + InputLanguage + """';
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.onresult = function(event) {
            let final_transcript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                }
            }
            if (final_transcript) { output.textContent = final_transcript.trim(); }
        };
        recognition.onerror = function(event) { console.error('Speech recognition error:', event.error); };
        recognition.start();
    </script></body></html>
    """

# --- TWO-STAGE LISTENING FUNCTIONS (Using WebDriverService) ---

def prepare_speech_engine():
    """
    Stage 1: Gets a clean browser instance from the central service.
    """
    print("🚀 Requesting new browser instance for STT...")
    driver = get_new_driver_instance()
    if driver:
        try:
            html_content = get_html_code()
            driver.get(f"data:text/html;charset=utf-8,{html_content}")
            print("✅ Speech engine is hot and ready.")
            return driver
        except Exception as e:
            print(f"❌ Error while loading HTML into new browser instance: {e}")
            driver.quit()
            return None
    return None

def capture_speech(driver):
    """
    Stage 2: Assumes the engine is already prepared and running.
    Captures the speech and then closes the engine.
    """
    if not driver:
        return "Error: Speech engine was not ready."

    try:
        print("🎤 Capturing speech...")
        last_speech_time = time.time()
        last_transcript = ""
        total_timeout = time.time() + 30

        while time.time() < total_timeout:
            text_element = driver.find_element(By.ID, "output")
            current_transcript = text_element.text if text_element else ""

            if current_transcript and current_transcript != last_transcript:
                last_speech_time = time.time()
                last_transcript = current_transcript
            
            if last_transcript and (time.time() - last_speech_time > SILENCE_TIMEOUT_SECONDS):
                print(f"🎤 Final Heard: '{last_transcript}' (Silence detected)")
                if "en" in InputLanguage.lower(): return last_transcript.capitalize()
                else: return mt.translate(last_transcript, "en", "auto").capitalize()

            time.sleep(0.1)

        if last_transcript:
            print(f"🎤 Final Heard: '{last_transcript}' (Total timeout reached)")
            return last_transcript.capitalize()

        return "I didn't hear anything, please try again."

    except Exception as e:
        print(f"❌ Error during speech capture: {e}")
        return "There was an issue with the speech recognition engine."
    
    finally:
        if driver:
            print("🛑 Closing STT browser instance.")
            driver.quit()