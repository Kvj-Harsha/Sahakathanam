# 📖 సహకథనం (Sahakathanam)

A collaborative storytelling web app where users take turns writing story segments in Indian languages, starting with Telugu.

> 🚧 Work in Progress: This project is being actively developed as part of Summer of Code 2025 at VISWAM.AI by the AI Developers Intern Team.
Expect frequent updates, feature rollouts, and experimental features as we build towards a fully collaborative, multilingual storytelling experience.

---

## 🧠 Idea

**Sahakathanam** is a chain-story builder designed to collect natural narrative text in regional languages. One user starts a story with a few lines, and others continue it, one segment at a time. Each contribution is stored locally (offline-first) and can be synced later for corpus collection.

---

## ⚙️ Tech Stack

| Layer        | Tech Used                   |
|--------------|-----------------------------|
| Frontend     | Streamlit                   |
| Storage      | JSON (local file-based DB)  |
| Offline Mode | Streamlit local caching     |
| Hosting      | Hugging Face Spaces         |
| Language     | Python 3                    |

---

## 🛣️ Project Roadmap

This app is structured in 3 progressive phases, starting from a minimal offline-capable collector to a fully AI-augmented storytelling engine.

---

### ✅ Phase 1: Basic Corpus Collector (MVP)

> 🕐 Timeline: Day 1

- Build a functional collaborative story-writing tool.
- Multilingual story creation (starting with Telugu).
- Offline-first: stories can be written without internet.
- Local JSON storage.
- Manual corpus upload/sync when network is available.

**Tech Used:**
- Streamlit
- Python 3
- JSON file storage
- Hugging Face Spaces for deployment

---

### 🤖 Phase 2: Light ML/NLP Enhancements

> 🕐 Timeline: Week 2

- Detect the language used in each input (e.g., Telugu, Hindi).
- Tag segments as "narrative" or "dialogue".
- Add metadata to each story segment to improve corpus quality.

**Example Output:**
```json
{
  "text": "ఒక ఊరిలో చిన్నారి ఉండేది.",
  "type": "narrative",
  "lang_detected": "te"
}
```
---
# Upcoming

> analytics dashboard