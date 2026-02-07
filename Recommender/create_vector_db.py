import json
import os
import shutil
import sys
from pathlib import Path

# --- UPDATED IMPORTS (Fixes ModuleNotFoundError) ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document  # <--- UPDATED IMPORT

# --- PATH CONFIGURATION ---
# 1. Get the 'faculty-assignment' root folder
BASE_DIR = Path(__file__).resolve().parent.parent 

# 2. Source Data (Where your Scraper saved the JSON)
DATA_PATH = BASE_DIR / "Scraper" / "Scraped_data" / "final_faculty_data.json"

# 3. Destination (Where the Vector DB will be saved)
DB_PERSIST_DIR = BASE_DIR / "Recommender" / "chroma_db"

def create_vector_db():
    print("STARTING: Vector Database Creation")
    
    # 1. Verify Data Exists
    if not DATA_PATH.exists():
        print(f"Error: Could not find data at {DATA_PATH}")
        print("   Did you run 'python Scraper/ingestion.py'?")
        return

    # 2. Load the JSON Data
    print(f"Loading data from: {DATA_PATH.name}")
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    
    # 3. Prepare Documents for Embedding
    documents = []
    
    for profile in data:
        # Construct the "Searchable Text"
        page_content = (
            f"Name: {profile.get('name', 'Unknown')}. "
            f"Designation: {profile.get('designation', '')}. "
            f"Specialization: {profile.get('specialization', '')}. "
            f"Research Interests: {profile.get('research', '')}. "
            f"Bio: {profile.get('bio', '')}. "
            f"Teaching: {profile.get('teaching', '')}."
        )
        
        # Metadata allows us to filter or retrieve specific links later
        metadata = {
            "id": profile.get("id"),
            "name": profile.get("name"),
            "profile_url": profile.get("profile_url"),
            "email": profile.get("email")
        }
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
    
    print(f"Processed {len(documents)} profiles into documents.")

    # 4. Initialize the Embedding Model
    print("Loading Embedding Model (all-MiniLM-L6-v2)...")
    try:
        embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Model Load Error: {e}")
        return

    # 5. Create and Persist the Database
    # If DB exists, delete it to ensure a fresh start
    if DB_PERSIST_DIR.exists():
        print("♻️  Removing old database to ensure freshness...")
        shutil.rmtree(DB_PERSIST_DIR)

    print("Generating Vectors and Saving to Disk (This may take a moment)...")
    
    # This single line does the heavy lifting: Embeds text -> Stores in DB
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_function,
        persist_directory=str(DB_PERSIST_DIR)
    )
    
    print(f"SUCCESS! Vector Database saved to: {DB_PERSIST_DIR}")
    # Note: New Chroma versions might not expose _collection publicly, but the file check is sufficient.

if __name__ == "__main__":
    create_vector_db()