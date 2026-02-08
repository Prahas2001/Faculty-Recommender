import google.generativeai as genai
import os
from dotenv import load_dotenv
from Recommender.inference import get_all_faculty_context

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chat_with_faculty(user_query):
    # 1. Get the text list of all faculty (Very low RAM usage)
    context_text = get_all_faculty_context()

    # 2. Build a smart prompt for Gemini
    prompt = f"""
    You are an academic advisor at DA-IICT. 
    User is looking for expertise in: "{user_query}"
    
    FACULTY DATABASE:
    {context_text}
    
    TASK:
    1. Select the top 3-5 faculty members who best match the query.
    2. Explain clearly WHY each one is a good fit.
    3. Include their Profile URL.
    4. Maintain a professional, helpful tone.
    """

    try:
        # 1.5-flash is extremely fast and has a huge memory for the list
        model = genai.GenerativeModel('gemini-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"