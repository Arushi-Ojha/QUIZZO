import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

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

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")


    try:
        response = await model.generate_content_async(prompt)
        return json.loads(response.text.strip())
    except Exception as e:
        print("❌ Gemini API Error:", e)
        return []
