# FacultyFinder: DA-IICT Faculty Data Pipeline

## Project Overview
**FacultyFinder** is a comprehensive Data Engineering pipeline designed to harvest, clean, and serve faculty profiles from the DA-IICT website.

The system scrapes data from 5 distinct faculty directories, consolidates them into a unified schema, and exposes the clean dataset via a REST API. This project serves as the **Data Infrastructure Layer** for a downstream Semantic Search Engine, allowing researchers to query faculty interests beyond simple keyword matching.

## Key Features
* **Automated Ingestion:** Scrapes Regular, Adjunct, Distinguished, Professor of Practice, and International Adjunct faculty.
* **Data Cleaning:**
    * Sanitizes email addresses (converts `[at]` to `@`).
    * Removes hidden UI artifacts (e.g., "displayNone" text).
    * Standardizes missing fields to `NULL` or empty strings.
* **Dual Storage Strategy:** Persists data to both a **SQLite Database** (`faculty_data.db`) for relational querying and a **JSON Artifact** (`final_faculty_data.json`) for portability.
* **Serving Layer:** A high-performance FastAPI server that exposes the dataset for downstream applications.

## Tech Stack
* **Language:** Python 3.10+
* **Web Scraping:** `BeautifulSoup4`, `Requests`
* **Data Processing:** `Pandas`, `SQLite3`
* **API Framework:** `FastAPI`, `Uvicorn`

---

## Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/FacultyFinder.git](https://github.com/YOUR_USERNAME/FacultyFinder.git)
    cd FacultyFinder
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

##  How to Run

### Step 1: Ingestion (Data Collection)
Run the ingestion script to crawl the websites, scrape the profiles, and clean the data.
```bash
python ingest.py
```
* **Action:** Scrapes 5 sources, cleans text, and saves to DB.
* **Output:** Creates `faculty_data.db` and `final_faculty_data.json`.
* **Success Indicator:** Look for `SUCCESS! Data exported...` in the terminal.

### Step 2: Serving (Start API)
Launch the FastAPI server to expose the cleaned data as a web service.
```bash
uvicorn main:app --reload
```
* **Action:** Loads `final_faculty_data.json` into memory and starts a local web server.
* **Output:** Server starts at `http://127.0.0.1:8000`.

### Step 3: Verification (Smoke Test)
Open your web browser and navigate to the interactive API documentation to test the system.
**Link:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | **Health Check.** Returns API status and total record count. |
| `GET` | `/faculty/all` | **Bulk Fetch.** Returns the complete dataset. (Used for vector embedding generation). |
| `GET` | `/faculty/{id}` | **Single Fetch.** Retrieves a specific faculty profile by their database ID. |

---

## Project Structure
```
FacultyFinder/
├── ingest.py                # Step 1: Main scraping and data cleaning logic
├── main.py                  # Step 2: FastAPI application server
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── final_faculty_data.json  # (Output) Cleaned dataset ready for use
└── faculty_data.db          # (Output) SQLite database
```