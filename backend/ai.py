import os
import json
import requests
from dotenv import load_dotenv
import time
import re

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://quizzeria-world.netlify.app",  # your Netlify frontend
    "X-Title": "Quizzeria AI Generator"
}

def extract_json_block(text):
    """Extract the first valid JSON array from messy AI output"""
    try:
        match = re.search(r'\[\s*{.*?}\s*]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("❌ Failed to extract JSON block:", e)
    return []

async def generate_quiz_questions(title, description, level):
    prompt = f"""
You are an expert quiz maker.

Generate exactly 20 multiple-choice questions based on the quiz below.

Quiz Title: {title}
Description: {description}
Difficulty Level: {level}

Each question must include:
- "question": the question text
- "A", "B", "C", "D": four options
- "correct": one of "A", "B", "C", or "D"

Respond with ONLY a JSON list of 20 dictionaries. Do NOT include explanation, intro, or markdown formatting.
    """

    body = {
        "model": "mistralai/mistral-7b-instruct",  # You can switch this to another OpenRouter model
        "messages": [
            {"role": "system", "content": "You are an AI quiz generator."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=body)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # Try parsing cleanly first
        try:
            return json.loads(content)
        except:
            return extract_json_block(content)

    except Exception as e:
        print("❌ OpenRouter API Error:", e)
        return []
