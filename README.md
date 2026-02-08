# FacultyFinder: DA-IICT Faculty Data Pipeline

## Project Overview

**Faculty Recommender** is an advanced AI discovery engine that transforms structured faculty data into an interactive, semantic-aware research consultant.

This component utilizes a **Long-Context LLM Architecture** powered by **Gemini 2.5 Flash** to perform deep semantic reasoning across the entire DA-IICT faculty corpus. Unlike traditional vector-search systems that rely on heavy local embedding models, this system implements a **"Zero-Infrastructure" RAG approach.** By injecting the full faculty directory directly into the model's expansive context window, the engine understands the nuanced relationship between a student’s research query and a professor's expertise—matching intent and sub-fields (e.g., "Deep Learning" to "Computer Vision") rather than just literal keywords.

The system is specifically engineered for **Resource Optimization**, replacing massive vector databases with a lightweight JSON-context retrieval strategy. This allows the production environment to maintain a stable memory footprint of **under 100MB RAM**, ensuring high-availability deployment on cloud-constrained environments like **Render's Free Tier.**

## Key Features: Faculty Recommender

* **Semantic Reasoning Engine:** Leverages **Gemini 2.5 Flash** to understand research intent and sub-field relationships rather than relying on simple keyword matching.
* **Long-Context Architecture:** Implements a "Zero-Infrastructure" RAG approach by injecting the full faculty corpus directly into the LLM's context window.
* **Memory-Optimized Deployment:** Specifically engineered to operate under a **100MB RAM** footprint, ensuring stable execution on **Render's Free Tier** (512MB limit).
* **Explanatory AI Logic:** Provides detailed natural language reasoning for every recommendation, highlighting the specific synergy between user queries and faculty profiles.
* **Lightweight Context Retrieval:** Utilizes a streamlined **JSON-based** "Source of Truth" to minimize latency and eliminate the overhead of local vector databases.
* **Hybrid Integration:** Seamlessly connects a **FastAPI** backend with a **Streamlit** frontend for a responsive, production-ready research discovery interface.

---

## Tech Stack: Faculty Recommender

* **Language:** Python 3.10+
* **AI Engine:** `Google Generative AI` (Gemini 2.5 Flash)
* **API Framework:** `FastAPI`, `Uvicorn`
* **Frontend UI:** `Streamlit`
* **Data Handling:** `JSON` (Lightweight Context Retrieval)
* **Environment Management:** `python-dotenv`

---

## Setup & Installation

### 1. Clone the Repository
    ```bash
    git clone [https://github.com/YOUR_USERNAME/faculty-recommender.git](https://github.com/YOUR_USERNAME/faculty-recommender.git)
    cd faculty-recommender
    ```

### 2.  **Create a Virtual Environment**
    It is recommended to use a virtual environment to manage dependencies and avoid conflicts.
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

### 3.  **Install Dependencies**
    This project uses a lightweight requirements.txt specifically optimized for environments with memory constraints (under 512MB RAM).
    ```bash
    pip install -r requirements.txt
    ```

### 4.  **Configure Environment Variables**
    Create a .env file in the root directory to securely store your API credentials.
    ```Plaintext
    GEMINI_API_KEY=your_google_ai_studio_key_here
    ```

---

## Workflow & Usage

### Step 1: Environment Configuration
Before launching the intelligence layer, ensure your Gemini API key is configured.
* **Action**: Create a `.env` file in the root directory.
* **Variable**: `GEMINI_API_KEY=your_google_ai_studio_key_here`

### Step 2: Backend Initialization (FastAPI)
Start the metadata and inference server. This layer handles the semantic context retrieval.
```bash
uvicorn Scraper.serving:app --reload
```
* **Process:** Loads the lightweight faculty_data.json into memory and prepares the Gemini-Flash inference engine.
* **Endpoint:** Access the API docs at http://127.0.0.1:8000/docs.

### Step 3: Frontend Deployment (Streamlit)
Launch the interactive research discovery dashboard.
```bash
streamlit run app.py
```
* **Action:** This will open a browser window at http://localhost:8501.


### Step 4: Semantic Discovery
Interact with the engine to find research matches.
* **Input:** Enter a research interest (e.g., "Quantum Computing" or "Graph Neural Networks") into the discovery bar.
* **Processing:** The system performs a Zero-Infrastructure RAG pass, injecting the faculty corpus into the LLM context.
* **Output:** Receive a ranked list of faculty members along with an AI-generated reasoning report explaining the research alignment.

---

## API Endpoints: Intelligence Layer

The following endpoints are exposed via the **FastAPI** backend to facilitate semantic discovery and metadata retrieval.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | **Health Check.** Returns API status and available discovery endpoints. |
| `GET` | `/faculty` | **Bulk Metadata.** Returns the complete curated faculty dataset from the JSON source. |
| `GET` | `/recommend` | **Semantic Inference.** Accepts a query `q` and returns Gemini-powered recommendations with reasoning. |

---

### Request Examples

#### 1. Faculty Recommendation (Semantic Search)
**Endpoint:** `/recommend?q={query}`
* **Example**: `/recommend?q=Heterogeneous+Graphs`
* **Response**:
```json
{
  "ai_response": "Based on the research profiles, Dr. [Name] is a top match due to their work in [Field]. Their recent projects in [Project] align with your interest in Graphs..."
}
```

#### 2. Faculty Metadata Fetch
**Endpoint:** `/faculty`
* **Description:** Useful for downstream applications needing the raw validated profiles (Name, Research Email, etc.).
* **Response**:
```json
[
  {
    "id": 1,
    "name": "Dr. Biswajit Mishra",
    "research": "Embedded Systems, VLSI",
    "email": "biswajit_mishra@daiict.ac.in",
    "specialization": "VLSI Design"
  }
]
```

---

## Project Structure
```
FacultyFinder/
├── Scraper/                 # Pillar 1: Ingestion & Metadata API
│   ├── ingestion.py         # Selenium extraction logic
│   ├── faculty_db.py        # SQLite schema & CRUD operations
│   ├── serving.py           # FastAPI metadata server
│   └── analysis.py          # Data health reports
├── Recommender/             # Pillar 2: AI Intelligence
│   ├── chat_engine.py       # Gemini 2.5 Flash reasoning logic
│   └── inference.py         # Context retrieval from JSON
├── faculty_data.json        # Unified "Semantic Source of Truth"
├── app.py                   # Streamlit Frontend Dashboard
└── requirements.txt         # Lightweight dependency list
```

---

## Dataset Statistics & Analysis


| Attribute | Value |
| :--- | :--- |
| **Total Observations** | 112 |
| **Total Columns** | 10 |
| **Data Types** | `int64` (1), `object` (9) |
| **Memory Usage** | 8.9+ KB |

---

### Column Schema & Completeness

| # | Column Name | Non-Null Count | Data Type | Status |
| :-- | :--- | :--- | :--- | :--- |
| 0 | **id** | 112 | `int64` | Full |
| 1 | **name** | 112 | `object` | Full |
| 2 | **designation** | 110 | `object` | Minor Missing |
| 3 | **email** | 112 | `object` | Full |
| 4 | **bio** | 72 | `object` | High Missing |
| 5 | **research** | 112 | `object` | Full |
| 6 | **publications** | 63 | `object` | High Missing |
| 7 | **teaching** | 72 | `object` | High Missing |
| 8 | **specialization** | 109 | `object` | Minor Missing |
| 9 | **profile_url** | 112 | `object` | Full |

---

### MISSING DATA BREAKDOWN

| Column | Missing (NaN) | Empty String | Total Empty | % Complete |
| :--- | :--- | :--- | :--- | :--- |
| **id** | 0 | 0 | 0 | **100.0%** |
| **name** | 0 | 0 | 0 | **100.0%** |
| **designation** | 2 | 0 | 2 | **98.2%** |
| **email** | 0 | 0 | 0 | **100.0%** |
| **bio** | 40 | 0 | 40 | **64.3%** |
| **research** | 0 | 0 | 0 | **100.0%** |
| **publications** | 49 | 0 | 49 | **56.2%** |
| **teaching** | 40 | 0 | 40 | **64.3%** |
| **specialization** | 3 | 0 | 3 | **97.3%** |
| **profile_url** | 0 | 0 | 0 | **100.0%** |

---

## Technical Challenges & Solutions

### **The 512MB RAM Bottleneck**
* **Challenge**: The initial deployment using `ChromaDB` and `Sentence-Transformers` (local embeddings) exceeded the **512MB RAM limit** on Render’s free tier, leading to persistent "Out of Memory" crashes.
* **Solution**: Re-engineered the architecture to a **JSON-Context Injection** model. By shifting the semantic processing to **Gemini 2.5 Flash**'s long-context window, we eliminated the need for heavy local vector databases.
* **Result**: Reduced the production memory footprint from **800MB+** to a stable **~90MB**, ensuring 100% uptime on free-tier infrastructure.

### **Handling Model Depreciation**
* **Challenge**: The retirement of earlier Gemini models (1.5 series) caused 404 endpoint errors during the transition to 2026 standards.
* **Solution**: Migrated the inference engine to the **Gemini 2.5 Flash** stable release, ensuring future-proof API calls and improved semantic extraction accuracy.

---

## License & Attribution
* **Data Source**: Publicly available faculty directories from the [DA-IICT Website](https://www.daiict.ac.in/).
* **AI Model**: Powered by Google Gemini 2.5.
* **License**: Distributed under the MIT License. See `LICENSE` for more information.

---
