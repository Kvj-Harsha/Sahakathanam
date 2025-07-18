# utils/helpers.py
from langdetect import detect
import re
from datetime import datetime

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def classify_segment_type(text):
    if re.search(r"[\"“”‘’].+?[\"“”‘’]", text):
        return "dialogue"
    elif re.search(r"(said|replied|అన్నాడు|అంది|बोला|कहा)", text, re.IGNORECASE):
        return "dialogue"
    return "narrative"

def generate_metadata(text):
    return {
        "language": detect_language(text),
        "type": classify_segment_type(text),
        "word_count": len(text.split()),
        "char_count": len(text)
    }

def format_timestamp(iso_str):
    try:
        return datetime.fromisoformat(iso_str).strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return iso_str
