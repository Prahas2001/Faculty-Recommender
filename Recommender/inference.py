import os
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Recommender" / "chroma_db"

def get_best_matches(query, k=3):
    """
    Takes a user query and returns best matches.
    LOADS MODEL ONLY ON DEMAND TO SAVE RAM.
    """
    # 1. Local Imports (Lazy Loading) - Saves ~200MB at startup
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    
    if not DB_PATH.exists():
        return {"error": "Vector DB not found. Please run create_vector_db.py"}

    # 2. Use CPU-only settings for the embedding model
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

    # 3. Connect to the DB
    vector_db = Chroma(
        persist_directory=str(DB_PATH), 
        embedding_function=embedding_function
    )

    # 4. Perform the search
    results = vector_db.similarity_search(query, k=k)

    # 5. Clean up output
    matches = []
    for doc in results:
        matches.append({
            "name": doc.metadata.get("name"),
            "email": doc.metadata.get("email"),
            "profile_url": doc.metadata.get("profile_url"),
            "excerpt": doc.page_content[:200] + "..."
        })
    
    # ⚠️ CRITICAL: Help Python clear memory after search
    del vector_db
    del embedding_function

    return matches