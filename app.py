import streamlit as st
import os

# ☁️ CLOUD CONFIGURATION
# If we are on Streamlit Cloud, use the secret URL.
# If we are local, default to localhost.
api_url = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

st.title("🎓 Faculty Recommender")
import requests
import re

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Faculty Insight Engine",
    page_icon="⚖️",
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
    
    /* Core Styling */
    .stApp { background-color: #F8FAFC; }
    
    /* Hero Header */
    .hero {
        background: #0F172A;
        padding: 3rem 2rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 4px solid #3B82F6;
    }
    .hero h1 { color: #F8FAFC; font-weight: 700; font-size: 2.5rem; margin: 0; }
    .hero p { color: #94A3B8; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; margin-top: 0.5rem; }

    /* Faculty Cards */
    .faculty-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease;
    }
    .faculty-card:hover { border-color: #3B82F6; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    
    .prof-name { color: #1E293B; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.5rem; }
    
    .rationale { color: #475569; line-height: 1.6; font-size: 1rem; margin-top: 0.5rem; }
    
    /* Intro Box Style */
    .intro-text {
        font-size: 1.1rem;
        color: #1E293B;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 4px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTION ---
def parse_and_clean_response(text):
    """
    Separates the intro from the list and cleans raw markdown.
    """
    # Split by the first numbered item (e.g., "1.")
    parts = re.split(r'(?=\n\d+\.)', text)
    
    # Clean the Intro Text (Remove ** and __)
    intro_text = parts[0].strip().replace('**', '').replace('__', '')
    
    faculty_list = []
    
    # Process each numbered part
    for part in parts[1:]:
        # Remove the number "1. " from the start
        clean_part = re.sub(r'^\n\d+\.\s*', '', part).strip()
        
        if clean_part:
            # Split into Name (Line 1) and Description (Rest)
            lines = clean_part.split('\n', 1)
            name = lines[0].strip().replace('**', '') # Clean the name
            desc = lines[1].strip() if len(lines) > 1 else ""
            
            # Clean description text
            desc = desc.replace('**', '').replace('*', '')
            
            faculty_list.append({"name": name, "desc": desc})
            
    return intro_text, faculty_list

# --- 4. UI LAYOUT ---
st.markdown('<div class="hero"><h1>Faculty Insight Engine</h1><p>Automated Expertise Mapping & Research Discovery</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ GATEWAY CONFIG")
    api_url = st.text_input("Endpoint", value="http://127.0.0.1:8000")
    st.markdown("---")
    st.info("💡 **Pro-Tip:** Use specific research terms like 'Heterogeneous Graphs' for better precision.")

_, center, _ = st.columns([1, 3, 1])

with center:
    query = st.text_input("", placeholder="Describe your research interest...")
    if st.button("Initialize Discovery"):
        if query:
            with st.spinner("Analyzing semantic alignments..."):
                try:
                    response = requests.get(f"{api_url}/recommend", params={"q": query})
                    if response.status_code == 200:
                        raw_text = response.json().get("ai_response", "")
                        
                        # Parse and Clean
                        intro, faculty = parse_and_clean_response(raw_text)
                        
                        # Display Clean Intro
                        if intro:
                            st.markdown(f'<div class="intro-text">{intro}</div>', unsafe_allow_html=True)
                        
                        # Display Clean Cards (No Badge)
                        for prof in faculty:
                            st.markdown(f"""
                            <div class="faculty-card">
                                <div class="prof-name">{prof['name']}</div>
                                <div class="rationale">{prof['desc']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("System Error: Backend unreachable.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")