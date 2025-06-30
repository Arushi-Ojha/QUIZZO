import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def generate_quiz_questions(title, description, level):
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

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.strip())
    except Exception as e:
        if "quota" in str(e).lower():
            print("❗ Gemini quota exceeded. Retrying after 30 seconds...")
            time.sleep(31)
            try:
                response = model.generate_content(prompt)
                return json.loads(response.text.strip())
            except Exception as inner_e:
                print("❌ Still failed after retry:", inner_e)
        else:
            print("❌ Gemini API Error:", e)
    return []

        