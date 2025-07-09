# app/services/summarizer.py

import os
from app.core.config import settings
import textwrap
import httpx

MAX_CHARS = 4000  # Safer input limit for LLMs

def chunk_text(text: str, max_chars=MAX_CHARS):
    return textwrap.wrap(text, max_chars, break_long_words=False, break_on_hyphens=False)

def build_prompt(text: str) -> str:
    return f"""
You are a helpful assistant. Read the following book content and:
1. Provide a concise summary (200–300 words).
2. List 5–10 key points in bullet form.

Book Text:
{text}
"""

def extract_summary_and_keypoints(raw_text: str) -> dict:
    lines = raw_text.splitlines()
    summary_lines = []
    bullet_points = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(("-", "•", "*", "1.", "2.", "3.")):
            bullet_points.append(line.lstrip("-•*0123456789. ").strip())
        else:
            summary_lines.append(line)

    summary = " ".join(summary_lines)
    return {
        "summary": summary,
        "key_points": bullet_points
    }

async def summarize_with_openrouter(text: str):
    chunks = chunk_text(text)
    prompt = build_prompt(chunks[0])  # use only the first chunk

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "openai/gpt-4o",
        "max_tokens": 3600,
        "messages": [
            {"role": "system", "content": "You are a book summarizer assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code != 200:
        print("OpenRouter error:", response.text)
        raise Exception("OpenRouter summarization failed")

    content = response.json()["choices"][0]["message"]["content"]
    return extract_summary_and_keypoints(content)
