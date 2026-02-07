import sys
from pathlib import Path

# --- IMPORTS ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- PATH CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent 
DB_PATH = BASE_DIR / "Recommender" / "chroma_db"

def test_search(query):
    print(f"\n🔎 SEARCHING FOR: '{query}'")
    print("-" * 50)

    # 1. Initialize the Embedding Model (Must be same as creation!)
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Load the Existing Database
    if not DB_PATH.exists():
        print("Error: DB not found. Run create_vector_db.py first.")
        return

    vector_db = Chroma(
        persist_directory=str(DB_PATH), 
        embedding_function=embedding_function
    )

    # 3. Perform Similarity Search (Get top 3 results)
    results = vector_db.similarity_search(query, k=3)

    # 4. Display Results
    if not results:
        print("No matches found.")
    
    for i, doc in enumerate(results, 1):
        name = doc.metadata.get("name", "Unknown")
        score = "N/A" # Chroma's basic search doesn't always return score visibly in this method
        
        print(f"#{i}: {name}")
        print(f"   Context Snippet: {doc.page_content[:150]}...") # Show first 150 chars
        print("-" * 20)

if __name__ == "__main__":
    # Test Queries
    test_search("Professor working on Graph Neural Networks")
    test_search("Who teaches VLSI?")