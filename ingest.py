import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import sqlite3
import logging
import re
from urllib.parse import urljoin
import pandas as pd
import os

# --- CONFIGURATION ---
DB_NAME = "faculty_data.db"
CSV_FILENAME = "final_faculty_data.csv"
JSON_FILENAME = "final_faculty_data.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- NETWORK SESSION ---
def create_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

http = create_session()

# --- DATABASE SETUP ---
def setup_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME) # Clean start
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT DEFAULT 'Regular',
            designation TEXT,
            email TEXT,
            bio TEXT,
            specialization TEXT,
            publications TEXT,
            teaching TEXT,
            research TEXT,
            profile_url TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(data):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO faculty
            (name, category, designation, email, bio, specialization, publications, teaching, research, profile_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'), data.get('category'), data.get('designation'), 
            data.get('email'), data.get('bio'), data.get('specialization'), 
            data.get('publications'), data.get('teaching'), data.get('research'), 
            data.get('url')
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Database Save Error: {e}")

# --- PARSING HELPERS ---
def parse_profile_text(soup):
    data = {"bio": [], "specialization": [], "publications": [], "teaching": [], "research": []}
    content_div = soup.find('div', class_='region-content') or soup.find('div', id='block-system-main') or soup.body
    
    lines = [line.strip() for line in content_div.get_text(separator='\n').split('\n') if line.strip()]
    current_section = None
    
    for line in lines:
        line_lower = line.lower()
        if "biography" in line_lower and len(line) < 50: current_section = "bio"
        elif "specialization" in line_lower and len(line) < 50: current_section = "specialization"
        elif "publication" in line_lower and len(line) < 50: current_section = "publications"
        elif "teaching" in line_lower and len(line) < 50: current_section = "teaching"
        elif "research" in line_lower and len(line) < 50: current_section = "research"
        elif current_section and len(line) > 3: data[current_section].append(line)

    return {k: " ".join(v).strip() if v else None for k, v in data.items()}

# --- SCRAPING MODULES ---

def scrape_regular():
    logging.info("--- Starting REGULAR Faculty ---")
    url = "https://www.daiict.ac.in/faculty"
    resp = http.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    for div in soup.find_all('div', class_='personalDetails'):
        try:
            link = div.find('h3').find('a')
            name = link.get_text(strip=True)
            profile_url = urljoin(url, link['href'])
            
            # Deep Scrape
            p_resp = http.get(profile_url)
            p_soup = BeautifulSoup(p_resp.content, 'html.parser')
            details = parse_profile_text(p_soup)
            
            # Email extraction
            email = "Unknown"
            contact = div.find('div', class_='contactDetails')
            if contact:
                match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', contact.get_text())
                if match: email = match.group(0)

            data = {
                "name": name, "category": "Regular", "url": profile_url, "email": email,
                "designation": div.find('div', class_='facultyEducation').get_text(strip=True) if div.find('div', class_='facultyEducation') else "Unknown",
                **details
            }
            save_to_db(data)
            logging.info(f"Saved: {name}")
        except Exception as e:
            logging.error(f"Error scraping {name if 'name' in locals() else 'unknown'}: {e}")

def scrape_adjunct_and_others():
    urls = {
        "Adjunct": "https://www.daiict.ac.in/adjunct-faculty",
        "International Adjunct": "https://www.daiict.ac.in/adjunct-faculty-international",
        "Professor of Practice": "https://www.daiict.ac.in/professor-practice",
        "Distinguished": "https://www.daiict.ac.in/distinguished-professor"
    }

    for category, url in urls.items():
        logging.info(f"--- Starting {category} ---")
        resp = http.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        items = soup.find_all('div', class_='personalDetail') or soup.find_all('div', class_='personalDetails') or soup.find_all('div', class_='views-row')
        
        for item in items:
            try:
                if not item.find('h3'): continue
                link = item.find('h3').find('a')
                if not link: continue
                
                name = link.get_text(strip=True)
                profile_url = urljoin(url, link['href'])
                
                data = {
                    "name": name, "category": category, "url": profile_url,
                    "email": "Unknown", "bio": None, "specialization": None, 
                    "publications": None, "teaching": None, "research": None,
                    "designation": "Unknown"
                }
                
                email_span = item.find('span', class_='facultyemail') or item.find('div', class_='contactDetails')
                if email_span:
                    data['email'] = email_span.get_text(strip=True).replace('[at]', '@').replace('[dot]', '.')

                edu_div = item.find('div', class_='facultyEducation')
                if edu_div: data['designation'] = edu_div.get_text(strip=True)

                spec_div = item.find_parent('li')
                if spec_div:
                    spec_text = spec_div.find('div', class_='areaSpecialization')
                    if spec_text: data['specialization'] = spec_text.get_text(strip=True)

                save_to_db(data)
                logging.info(f"Saved: {name}")

            except Exception as e:
                logging.error(f"Skipping row: {e}")

def export_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM faculty", conn)
    
    # Feature Engineering for Search
    df['search_text'] = df.apply(lambda row: " | ".join([
        str(row['name']), str(row['category']), str(row['specialization'] or ''), str(row['bio'] or '')
    ]), axis=1)
    
    df.to_csv(CSV_FILENAME, index=False)
    df.to_json(JSON_FILENAME, orient='records', indent=4)
    print(f"\n✅ SUCCESS! Data exported to {CSV_FILENAME} and {JSON_FILENAME}")
    conn.close()

if __name__ == "__main__":
    setup_database()         
    scrape_regular()         
    scrape_adjunct_and_others() 
    export_data()