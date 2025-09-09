# --- IMPORTS ---
# Standard library imports
import asyncio
import os
import sys
from random import randint
from time import sleep
from datetime import datetime

# Third-party imports
import httpx
from PIL import Image, UnidentifiedImageError
from dotenv import get_key

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "Data")

# --- UPGRADED IMAGE GENERATION MODEL ---
# Using the corrected URL for the playground-v2.5 model.
API_URL = "https://api-inference.huggingface.co/models/playgroundai/playground-v2.5-1024px-aesthetic"
headers = {"Authorization": f"Bearer {get_key('.env','HuggingFaceAPIKey')}"}

# --- ASYNCHRONOUS API QUERY ---
async def query_api(payload: dict, client: httpx.AsyncClient):
    """Sends a single request to the Hugging Face API."""
    try:
        response = await client.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        if response.headers.get("content-type", "").startswith("application/json"):
            print(f"❌ Hugging Face API Error: {response.json()}")
            return None
        
        return response.content

    except httpx.RequestError as e:
        print(f"❌ Network request failed: {e}")
        return None
    except httpx.HTTPStatusError as e:
        # Specifically check for rate limit errors
        if e.response.status_code in [429, 503]:
             print(f"❌ API Error: You have likely hit the monthly usage limit or a rate limit. (Status: {e.response.status_code})")
        else:
            print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
        return None

# --- IMAGE GENERATION LOGIC ---
async def generate_images(prompt: str):
    """Generates a batch of 4 images concurrently."""
    print("🎨 Generating images with Playground v2.5 model...")
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        tasks = []
        for _ in range(4):
            full_prompt = f"{prompt}, 4k, photorealistic, cinematic lighting, ultra details"
            payload = {"inputs": full_prompt, "parameters": {"seed": randint(0, 1000000)}}
            tasks.append(asyncio.create_task(query_api(payload, client)))

        image_bytes_list = await asyncio.gather(*tasks)

    saved_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            try:
                os.makedirs(DATA_DIR, exist_ok=True)
                file_path = os.path.join(DATA_DIR, f"image_{timestamp}_{i+1}.jpg")
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                saved_files.append(file_path)
                print(f"✅ Image saved to {file_path}")
            except IOError as e:
                print(f"❌ Error saving file: {e}")

    return saved_files

# --- SYNCHRONOUS WRAPPER ---
def run_generation_and_display(prompt: str):
    """Main synchronous function to run the async logic and open the images."""
    if not prompt:
        print("❌ Error: No prompt provided.")
        return

    saved_files = asyncio.run(generate_images(prompt))

    if not saved_files:
        print("⚠️ No images were generated.")
        return

    for fpath in saved_files:
        try:
            img = Image.open(fpath)
            img.show()
            sleep(1)
        except (IOError, UnidentifiedImageError) as e:
            print(f"⚠️ Could not open image {fpath}: {e}")
    
    try:
        from TextToSpeech import TextToSpeech
        TextToSpeech("I have finished generating the images and opened them for you.")
    except Exception as e:
        print(f"Could not announce completion: {e}")

# --- COMMAND-LINE ENTRY POINT ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_prompt = " ".join(sys.argv[1:])
        run_generation_and_display(input_prompt)
    else:
        print("Usage: python ImageGeneration.py <your_image_prompt>")