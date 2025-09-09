# In Backend/TextToSpeech.py

# --- IMPORTS ---
import pygame
import asyncio
import os
import sys
from time import sleep, time
from dotenv import dotenv_values
import edge_tts

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Backend.InterruptService import is_interrupted, reset_interrupt

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-GB-SoniaNeural")
DATA_DIR = r"Data" # Define the directory for speech files

# --- NEW: Cleanup function for old speech files ---
def cleanup_speech_files():
    """Deletes speech.mp3 files older than 5 minutes."""
    try:
        for filename in os.listdir(DATA_DIR):
            if filename.startswith("speech_") and filename.endswith(".mp3"):
                file_path = os.path.join(DATA_DIR, filename)
                # Check if the file is older than 300 seconds (5 minutes)
                if (time() - os.path.getmtime(file_path)) > 300:
                    os.remove(file_path)
    except Exception as e:
        print(f"⚠️ Warning: Could not clean up old speech files: {e}")


# --- REVISED ASYNC TTS GENERATION ---
async def TextToAudioFile(text: str, file_path: str):
    """Asynchronously generates a uniquely named MP3 file from text."""
    try:
        communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
        await communicate.save(file_path)
        return True
    except Exception as e:
        print(f"❌ Error generating speech file with edge-tts: {e}")
        return False

# --- REVISED CORE TTS LOGIC ---
def TTS(Text: str):
    """
    Generates and plays a unique audio file to prevent resource conflicts.
    """
    reset_interrupt()
    
    # --- NEW: Generate a unique filename for each speech act ---
    timestamp = int(time() * 1000)
    speech_file_path = os.path.join(DATA_DIR, f"speech_{timestamp}.mp3")

    try:
        # Generate the audio file
        file_created = asyncio.run(TextToAudioFile(Text, speech_file_path))
        if not file_created: return

        # Play the uniquely named file
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if is_interrupted():
                print("🛑 TTS INTERRUPTED! Stopping playback.")
                pygame.mixer.music.stop()
                return
            sleep(0.05)

    except Exception as e:
        print(f"❌ Error in TTS playback: {e}")
    
    finally:
        # The mixer itself is persistent, but we don't need to do anything with the file here.
        # The cleanup function will handle old files on the next run.
        pass

# --- REVISED MAIN FUNCTION ---
def TextToSpeech(Text: str):
    """Main entry point for text-to-speech. Cleans up old files."""
    if not Text or not Text.strip(): return
    
    # Run cleanup duty before generating new speech
    cleanup_speech_files()
    
    TTS(Text)