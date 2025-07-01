import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def generate_quiz_questions(title, description, level):
    prompt = f"""
    Generate 20 MCQs in JSON format with fields:
"question", "A", "B", "C", "D", "correct"

Topic: {title}
Desc: {description}
Level: {level}
Only JSON array.
    """

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        response = model.generate_content(prompt)

        # ✅ Properly extract the response content
        content = response.candidates[0].content.parts[0].text.strip()
        print("📥 Gemini Raw Output:\n", content)

        # ✅ Safely parse the JSON
        return json.loads(content)

    except Exception as e:
        # If quota error, wait and retry once
        if "quota" in str(e).lower():
            print("❗ Gemini quota exceeded. Retrying after 30 seconds...")
            time.sleep(31)
            try:
                response = model.generate_content(prompt)
                content = response.candidates[0].content.parts[0].text.strip()
                print("📥 Gemini Raw Output (retry):\n", content)
                return json.loads(content)
            except Exception as inner_e:
                print("❌ Still failed after retry:", inner_e)
        else:
            print("❌ Gemini API Error:", e)

    return []
