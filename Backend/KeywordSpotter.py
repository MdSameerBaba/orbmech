# In Backend/KeywordSpotter.py

import os
import struct
import threading
from dotenv import dotenv_values

import pvporcupine
import sounddevice as sd

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
PICOVOICE_ACCESS_KEY = env_vars.get("PicovoiceAccessKey")

# --- REDUNDANCY FIX: Use the central Interrupt Service ---
# We now import the official flag functions to ensure the whole app is synchronized.
from Backend.InterruptService import set_interrupt, reset_interrupt
# --- END FIX ---

# --- STATE-OF-THE-ART KEYWORD SPOTTER ---
class PorcupineSpotter(threading.Thread):
    def __init__(self, access_key: str, keywords: list):
        super().__init__()
        self._access_key = access_key
        self._keywords = keywords
        self._stop_event = threading.Event()
        self.daemon = True

    def run(self):
        porcupine = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(access_key=self._access_key, keywords=self._keywords)
            audio_stream = sd.InputStream(
                samplerate=porcupine.sample_rate, channels=1,
                blocksize=porcupine.frame_length, dtype='int16'
            )
            
            print(f"🤫 Professional barge-in listener started. Say '{self._keywords[0].upper()}' to interrupt.")

            while not self._stop_event.is_set():
                pcm, _ = audio_stream.read(porcupine.frame_length)
                pcm = pcm.flatten()
                result = porcupine.process(pcm)

                if result >= 0:
                    print(f"🛑 Keyword '{self._keywords[result]}' detected! Triggering interrupt.")
                    # Use the official set_interrupt function
                    set_interrupt()
                    self._stop_event.set()

        except pvporcupine.PorcupineError as e:
            print(f"❌ Porcupine Error: {e}")
        except Exception as e:
            print(f"❌ Error in keyword spotter thread: {e}")
        finally:
            if porcupine is not None:
                porcupine.delete()
            # --- BUG FIX: Corrected the 'if' statement ---
            if audio_stream is not None:
                audio_stream.close()
            # --- END FIX ---
            print("🤫 Barge-in listener stopped.")

    def stop(self):
        self._stop_event.set()

# --- PUBLIC FUNCTIONS TO CONTROL THE SPOTTER ---
spotter_instance = None

def start_keyword_spotter():
    global spotter_instance
    if spotter_instance is None or not spotter_instance.is_alive():
        # Use the official reset_interrupt function
        reset_interrupt()
        spotter_instance = PorcupineSpotter(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=['terminator']
        )
        spotter_instance.start()

def stop_keyword_spotter():
    global spotter_instance
    if spotter_instance is not None and spotter_instance.is_alive():
        spotter_instance.stop()
        spotter_instance.join()
        spotter_instance = None