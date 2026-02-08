import json
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

print("⏳ Extracting data from local Chroma DB...")
# Use your current local settings to load the DB
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="Recommender/chroma_db", embedding_function=embedding)

data = []
results = db.get() # Retrieves all IDs, Metadatas, and Documents

for i in range(len(results['ids'])):
    meta = results['metadatas'][i]
    content = results['documents'][i]
    data.append({
        "name": meta.get('name', 'Unknown'),
        "email": meta.get('email', ''),
        "profile_url": meta.get('profile_url', ''),
        "research": content 
    })

with open("faculty_data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Created 'faculty_data.json' with {len(data)} profiles.")