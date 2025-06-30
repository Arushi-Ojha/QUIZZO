
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("AIzaSyDMgrB3SaJWFkN2ZgKyYKq7fiK3UYsDEmU"))

def generate_quiz_questions(title, description, level):
    prompt = f"""
    Generate 20 MCQs based on the following quiz:
    Title: {title}
    Description: {description}
    Difficulty Level: {level}

    Each question must include:
    - question
    - option A
    - option B
    - option C
    - option D
    - correct answer (A/B/C/D)

    Output should be in JSON list format with keys: "question", "A", "B", "C", "D", "correct"
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    print("🔍 Raw Gemini Response:", response.text)

    # Extract JSON from response
    try:
        import json
        return json.loads(response.text.strip())
    except Exception as e:
        print("Error:", e)
        return []
