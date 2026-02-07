import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API Key not found in .env")
    exit()

client = genai.Client(api_key=api_key)

print(f"Checking available models for key ending in ...{api_key[-4:]}")
print("-" * 50)

try:
    # List all models
    for m in client.models.list():
        # We only care about models that can "generateContent" (Chat models)
        if "generateContent" in m.supported_generation_methods:
            print(f"FOUND: {m.name}")
            
except Exception as e:
    print(f"API Error: {e}")
    print("\n💡 TIP: If this says '403' or 'Quota', your key might need billing enabled.")