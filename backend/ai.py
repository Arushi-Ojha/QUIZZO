import os
import json
import requests
from dotenv import load_dotenv
import time

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://quizzeria-world.netlify.app/ai",
    "X-Title": "Quizzeria AI Quiz Generator"
}

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

Output as a valid JSON list of 20 dictionaries with keys: "question", "A", "B", "C", "D", "correct".
    """

    body = {
        "model": "mistralai/mistral-7b-instruct",  # or "anthropic/claude-3-haiku"
        "messages": [
            {"role": "system", "content": "You are an AI quiz generator."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=body)
        res.raise_for_status()
        answer = res.json()["choices"][0]["message"]["content"]
        return json.loads(answer.strip())
    except Exception as e:
        print("❌ OpenRouter API Error:", e)
        return []
