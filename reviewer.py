import streamlit as st

import os
import requests
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

GROK_API_KEY = os.getenv("GROK_API_KEY") or st.secrets.get("GROK_API_KEY", None)

GROK_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def review_with_llm(code, issues, level="senior", provider=None):

    if level == "junior":
        tone = "friendly and educational, like a mentor teaching a beginner."
    else:
        tone = "strict and production-grade, focusing on best practices for real-world software."

    prompt = f"""
You are a {level} software engineer reviewing code {tone}.
Analyze the following code.

Detected static issues:
{', '.join(issues) if issues else 'None'}

Code:
{code}

Return your review in this exact structure:

1. Bugs:
2. Bad practices:
3. Improvements:
4. Fix suggestions:
5. Explanation:
"""

    if provider is None:
        if GROK_API_KEY:
            provider = "grok"
        else:
            provider = "ollama"

    logger.info(f"Selected provider: {provider}")

    # ---------------- OLLAMA ----------------
    if provider == "ollama":
        try:
            response = requests.post(
                f"{OLLAMA_API_URL}/api/generate",
                json={
                    "model": "deepseek-coder:6.7b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Error: No response received from Ollama.")
            else:
                return f"Error: Ollama API Error ({response.status_code})\n{response.text}"

        except Exception as e:
            return f"Error: Ollama request failed - {str(e)}"

    # ---------------- GROQ ----------------
    elif provider == "grok":
        if not GROK_API_KEY:
            return "Error: GROK_API_KEY not found in .env or environment variables."

        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post(GROK_API_URL, headers=headers, json=payload, timeout=60)

            if response.status_code != 200:
                return f"Error: Groq API Error ({response.status_code})\n{response.text}"

            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]

            return f"Error: Unexpected response format:\n{json.dumps(result, indent=2)}"

        except Exception as e:
            return f"Error: Groq request failed - {str(e)}"

    else:
        return f"Error: Unknown provider '{provider}'"
