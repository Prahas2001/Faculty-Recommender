import os
from fastapi import FastAPI, HTTPException
import sys
from pathlib import Path

# --- ROBUST IMPORT SETUP ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
sys.path.append(str(CURRENT_DIR))
sys.path.append(str(ROOT_DIR))

# --- IMPORTS ---
# We ONLY import the logic we need. 
# Make sure faculty_db.py does NOT import torch or chromadb!
import faculty_db as storage 
from Recommender.chat_engine import chat_with_faculty 

app = FastAPI(title="DA-IICT Faculty AI")

@app.get("/")
def home():
    return {
        "status": "Active", 
        "mode": "Lightweight JSON",
        "endpoints": ["/faculty", "/recommend?q=..."]
    }

@app.get("/faculty")
def get_all():
    """Return the entire dataset."""
    return storage.get_all_faculty()

@app.get("/recommend")
def recommend(q: str):
    print(f"--- 🚀 Query Received: {q} ---")
    try:
        # This now uses the JSON + Gemini logic (Low RAM)
        response_text = chat_with_faculty(q)
        return {"ai_response": response_text}
    except Exception as e:
        print(f"🛑 Error: {str(e)}")
        return {"error": "System is warming up or busy. Please try again."}

if __name__ == "__main__":
    import uvicorn
    # Local dev remains the same
    uvicorn.run(app, host="127.0.0.1", port=8000)
    