import os

# 1. Force the app to use only 1 CPU thread
# This prevents the server from spawning multiple threads that eat RAM
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# 2. Prevent PyTorch from loading CUDA drivers (Saves ~50-100MB RAM)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# 3. Optimize Python's own memory handling
os.environ["PYTHONHASHSEED"] = "0"

from fastapi import FastAPI, HTTPException
import sys
from pathlib import Path


# --- ROBUST IMPORT SETUP ---
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
sys.path.append(str(CURRENT_DIR))
sys.path.append(str(ROOT_DIR))

# --- IMPORTS ---
import faculty_db as storage 
from Recommender.chat_engine import chat_with_faculty 

app = FastAPI(title="DA-IICT Faculty AI", description="Hybrid Search: SQL + RAG AI")

@app.get("/")
def home():
    return {
        "status": "Active", 
        "endpoints": [
            "/faculty (List all)", 
            "/faculty/search?q=AI (Keyword Search)",
            "/recommend?q=Deep Learning (AI Analysis)"
        ]
    }

@app.get("/faculty")
def get_all():
    """Return the entire dataset (SQL Source)."""
    return storage.get_all_faculty()

@app.get("/faculty/search")
def search(q: str):
    """
    Legacy SQL Search.
    Finds exact text matches (e.g., 'Mishra' finds 'Biswajit Mishra').
    """
    results = storage.search_faculty(q)
    if not results:
        raise HTTPException(status_code=404, detail="No matches found.")
    return results

@app.get("/recommend")
def recommend(q: str):
    print(f"--- Processing Query: {q} ---")
    try:
        print("Step 1: Calling chat_with_faculty...")
        response_text = chat_with_faculty(q)
        print("Step 2: Success!")
        return {"ai_response": response_text}
    except Exception as e:
        print(f"🛑 CRASH IN SERVING: {str(e)}")
        return {"error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)