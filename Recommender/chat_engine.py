import os
import sys
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# --- SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not found! Did you create the .env file?")

# Import Search Logic
sys.path.append(str(BASE_DIR))
from Recommender.inference import get_best_matches

def get_working_model_url():
    """
    Dynamically asks Google which Gemini model is available for this Key.
    """
    print("🔍 Detecting available Gemini models...")
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(list_url)
        data = response.json()
        
        # Look for the first valid Gemini model
        if "models" in data:
            for m in data["models"]:
                name = m["name"] # e.g., "models/gemini-1.5-flash-001"
                methods = m.get("supportedGenerationMethods", [])
                
                # We need a model that supports 'generateContent' and is 'gemini'
                if "generateContent" in methods and "gemini" in name:
                    print(f"Auto-selected model: {name}")
                    # Return the URL for generation
                    return f"https://generativelanguage.googleapis.com/v1beta/{name}:generateContent?key={api_key}"
                    
    except Exception as e:
        print(f"Model Detection Failed: {e}")

    # FALLBACK: If detection fails, try the standard stable endpoint
    print("detection failed, using fallback.")
    return f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

# Get the URL once at startup
GENERATE_URL = get_working_model_url()

def chat_with_faculty(user_query):
    print(f"Searching database for: {user_query}...")
    
    # A. RETRIEVAL
    matches = get_best_matches(user_query, k=3)
    if not matches:
        return "I couldn't find any faculty members matching that description."

    # B. AUGMENTATION
    context_text = ""
    for i, m in enumerate(matches, 1):
        context_text += f"\n{i}. {m['name']} ({m['email']})\n"
        context_text += f"   Profile: {m['profile_url']}\n"
        context_text += f"   Summary: {m['excerpt']}\n"

    # C. GENERATION
    prompt = f"""
    You are a helpful assistant for DA-IICT students.
    User Question: "{user_query}"
    
    Relevant Faculty Data:
    {context_text}
    
    Task:
    Recommend these professors. Explain WHY they are a match.
    """
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(GENERATE_URL, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Connection Error: {e}"

if __name__ == "__main__":
    print("Thinking...")
    answer = chat_with_faculty("Who is working on Deep Learning?")
    print("\n" + "="*50)
    print(answer)
    print("="*50)

