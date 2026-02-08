import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "faculty_data.json"

def get_all_faculty_context():
    """Reads the JSON file and returns a text summary for Gemini."""
    if not DATA_PATH.exists():
        return "No faculty data available."
    
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    
    context_list = []
    for i, p in enumerate(data):
        # We give Gemini the name, URL, and a snippet of research
        context_list.append(f"{i+1}. {p['name']} ({p['profile_url']}): {p['research'][:400]}...")
    
    return "\n".join(context_list)