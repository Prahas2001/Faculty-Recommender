import os
import gc # Garbage Collection
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "Recommender" / "chroma_db"

def get_best_matches(query, k=3):
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    
    if not DB_PATH.exists():
        return {"error": "Vector DB not found on server."}

    # Use the SMALLEST possible model (paraphrase-MiniLM-L3-v2)
    embedding_function = HuggingFaceEmbeddings(
        model_name="paraphrase-MiniLM-L3-v2",
        model_kwargs={'device': 'cpu'}
    )

    vector_db = Chroma(
        persist_directory=str(DB_PATH), 
        embedding_function=embedding_function
    )

    results = vector_db.similarity_search(query, k=k)

    matches = []
    for doc in results:
        matches.append({
            "name": doc.metadata.get("name"),
            "email": doc.metadata.get("email"),
            "profile_url": doc.metadata.get("profile_url"),
            "excerpt": doc.page_content[:200]
        })
    
    # 🧹 MANUALLY CLEAR MEMORY
    del vector_db
    del embedding_function
    gc.collect() 

    return matches
