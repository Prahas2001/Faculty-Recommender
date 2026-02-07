from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Recommender" / "chroma_db"

# Load the model ONCE when the script starts (Optimization)
# This prevents reloading the 80MB model for every single search
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_best_matches(query, k=3):
    """
    Takes a user query (e.g., "AI for healthcare")
    Returns a list of best matching faculty profiles.
    """
    if not DB_PATH.exists():
        return {"error": "Vector DB not found. Please run create_vector_db.py"}

    # Connect to the DB
    vector_db = Chroma(
        persist_directory=str(DB_PATH), 
        embedding_function=embedding_function
    )

    # Perform the search
    results = vector_db.similarity_search(query, k=k)

    # Clean up the output for the API
    matches = []
    for doc in results:
        matches.append({
            "name": doc.metadata.get("name"),
            "email": doc.metadata.get("email"),
            "profile_url": doc.metadata.get("profile_url"),
            "excerpt": doc.page_content[:200] + "..." # Show a preview of why they matched
        })
    
    return matches
