# utils/ai_utils.py

import requests
import os

# Get your HF token from environment or secret config (e.g., Hugging Face Spaces)
HF_TOKEN = os.getenv("HF_TOKEN")

# Model endpoint
API_URL = "https://api-inference.huggingface.co/models/Telugu-LLM-Labs/Indic-gemma-7b-finetuned-sft-Navarasa-2.0"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def format_prompt(text, language="Telugu"):
    """
    Wraps user input for a continuation-style prompt in a story context.
    """
    return f"<s>[INST] Continue this story in {language}:\n{text.strip()} [/INST]"

def suggest_next_line(prompt_text, language="Telugu"):
    """
    Sends formatted prompt to Indic-Gemma model and returns generated continuation.
    """
    prompt = format_prompt(prompt_text, language)
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.9,
            "top_p": 0.95,
            "return_full_text": False
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)
        if response.status_code == 200:
            result = response.json()
            return result[0]["generated_text"].strip() if result else "⚠️ No output from model."
        else:
            return f"⚠️ API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Exception: {str(e)}"
