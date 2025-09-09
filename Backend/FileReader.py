# In Backend/FileReader.py
import fitz # The PyMuPDF library
from groq import Groq
from dotenv import dotenv_values
import os

# --- CONFIGURATION ---
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

try:
    client = Groq(api_key=GroqAPIKey)
except Exception as e:
    print(f"❌ Failed to initialize Groq client in FileReader.py: {e}"); client = None

# --- CORE FUNCTIONS ---
def get_text_from_pdf(filepath: str) -> str:
    """Extracts all text content from a given PDF file."""
    try:
        print(f"📖 Reading PDF: {filepath}")
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        print(f"✅ Extracted {len(text)} characters from PDF.")
        return text
    except Exception as e:
        print(f"❌ Error reading PDF file: {e}")
        return f"Error: Could not read the PDF file. Details: {e}"

def summarize_text(text: str) -> str:
    if not client:
        return "Cannot summarize text because the AI model is not available."
    if text.startswith("Error:"):
        return text

    print("🤖 Generating summary...")
    summarization_prompt = f"""
    You are a highly skilled AI assistant specializing in text analysis and summarization.
    Based on the following text, provide a concise, well-structured summary.
    TEXT TO SUMMARIZE:\n---\n{text[:8000]}\n---\nPlease provide the summary below.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": summarization_prompt}],
            stream=False
        )
        # FIX: Correct response parsing
        summary = completion.choices[0].message.content
        if not summary:
            summary = "⚠️ The AI returned an empty response."
        print("✅ Summary generated.")
        return summary
    except Exception as e:
        print(f"❌ Error during summarization API call: {e}")
        return f"Error: The AI model failed to generate a summary. Details: {e}"


if __name__ == "__main__":
    # 1. Define the path to your test document
    # The '../' goes up one level from 'Backend' to the main project folder
    test_pdf_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'test_document.pdf')

    print("--- STARTING MANUAL TEST: FileReader.py ---")

    # 2. Check if the test file exists
    if not os.path.exists(test_pdf_path):
        print(f"❌ TEST FAILED: The test file was not found at '{test_pdf_path}'")
        print("Please create a 'test_document.pdf' file and place it in the 'Data' folder.")
    else:
        # 3. Test the text extraction function
        print("\n--- Testing PDF Text Extraction ---")
        extracted_text = get_text_from_pdf(test_pdf_path)

        if not extracted_text.startswith("Error:"):
            print("\n--- First 500 characters of extracted text: ---")
            print(extracted_text[:500])
            print("\n-------------------------------------------------")
            
            # 4. If extraction is successful, test the summarization function
            print("\n--- Testing Text Summarization ---")
            summary = summarize_text(extracted_text)
            
            if not summary.startswith("Error:"):
                print("\n--- GENERATED SUMMARY: ---")
                print(summary)
                print("\n--------------------------")
                print("\n✅ TEST SUCCEEDED!")
            else:
                print(f"\n❌ TEST FAILED: Summarization returned an error.")
                print(summary)
        else:
            print(f"\n❌ TEST FAILED: Text extraction returned an error.")
            print(extracted_text)
    
    print("\n--- MANUAL TEST COMPLETE ---")