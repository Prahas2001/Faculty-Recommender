from fastapi import FastAPI, HTTPException
import json
import os
from typing import List, Dict, Any

DATA_FILE = "final_faculty_data.json"

app = FastAPI(title="FacultyFinder API")
faculty_db: List[Dict[str, Any]] = []

@app.on_event("startup")
async def load_data():
    global faculty_db
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            faculty_db = json.load(f)
        print(f"✅ API Ready: Loaded {len(faculty_db)} faculty records.")
    else:
        print("⚠️ Data file not found. Run ingest.py first!")

@app.get("/")
async def root():
    return {"status": "active", "total_faculty": len(faculty_db)}

@app.get("/faculty/all")
async def get_all_faculty():
    return faculty_db

@app.get("/faculty/{faculty_id}")
async def get_faculty(faculty_id: int):
    result = next((item for item in faculty_db if item.get("id") == faculty_id), None)
    if result: return result
    raise HTTPException(status_code=404, detail="Faculty not found")