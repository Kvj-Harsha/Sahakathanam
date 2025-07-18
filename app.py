import streamlit as st
import json
import os
import uuid
from datetime import datetime
from utils.helpers import generate_metadata, format_timestamp

# Constants
STORY_FILE = "storage/stories.json"
os.makedirs("storage", exist_ok=True)

# Load existing stories or create empty structure
def load_stories():
    if os.path.exists(STORY_FILE):
        with open(STORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                return {}
    return {}

# Save stories to file
def save_stories(stories):
    with open(STORY_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

# Initialize session state
if "stories" not in st.session_state:
    st.session_state.stories = load_stories()

# UI Setup
st.set_page_config(page_title="Sahakathanam", layout="wide")
st.sidebar.title("📖 సహకథనం (Sahakathanam)")
st.sidebar.markdown("A Collaborative Storytelling Platform")

# Sidebar inputs
language = st.sidebar.selectbox("Language", ["Telugu", "Hindi", "Kannada", "Tamil", "Malayalam"])
username = st.sidebar.text_input("Your Name", value="anon", max_chars=30)

# Suggested titles per language
hot_titles = {
    "Telugu": ["రామాయణ కథ", "తెనాలి రామకృష్ణ కథ", "బిర్బల్ కథలు"],
    "Hindi": ["रामायण कथा", "तेनालीराम की कहानी", "अकबर-बीरबल"]
}

st.title("🌱 Collaborative Storytelling in Indian Languages")
tab1, tab2 = st.tabs(["🆕 Start a New Story", "✍️ Continue Existing Story"])

# ------------------- Tab 1 -------------------
with tab1:
    st.subheader("Start a New Story")

    if language in hot_titles:
        st.markdown("**Suggested Titles:**")
        for t in hot_titles[language]:
            st.markdown(f"- {t}")

    title = st.text_input("Story Title", max_chars=100, key="new_title")
    initial_text = st.text_area("Opening Lines (2-3 sentences)", max_chars=500, height=150, key="initial_text")

    if st.button("🚀 Submit New Story"):
        existing_titles = [
            v["title"].strip().lower()
            for v in st.session_state.stories.values()
            if v.get("language") == language
        ]

        if not title or not initial_text:
            st.warning("Please provide both a title and the initial text.")
        elif title.strip().lower() in existing_titles:
            st.warning("A story with this title already exists in the selected language.")
        else:
            story_id = str(uuid.uuid4())
            st.session_state.stories[story_id] = {
                "title": title.strip(),
                "language": language,
                "segments": [
                    {
                        "text": initial_text.strip(),
                        "timestamp": datetime.now().isoformat(),
                        "user": username.strip(),
                        "coords": [17.3850, 78.4867],
                        "metadata": generate_metadata(initial_text.strip())
                    }
                ]
            }
            save_stories(st.session_state.stories)
            st.success("✅ Story created successfully!")

# ------------------- Tab 2 -------------------
with tab2:
    st.subheader("Continue a Story")

    stories = st.session_state.stories
    filtered_stories = {v["title"]: k for k, v in stories.items() if v.get("language") == language}
    selected_title = st.selectbox("Choose a story to continue", ["--"] + list(filtered_stories.keys()))

    if selected_title != "--":
        story_id = filtered_stories[selected_title]
        selected_story = stories[story_id]
        segments = selected_story["segments"]

        with st.expander("📖 Show Full Story"):
            for i, segment in enumerate(segments):
                st.markdown(f"**Part {i+1}** — *{segment['user']}* ({format_timestamp(segment['timestamp'])})")
                st.write(segment["text"])
                meta = segment.get("metadata", {})
                st.caption(
                    f"🈯 Language: {meta.get('language', '-')}, 🧠 Type: {meta.get('type', '-')}, "
                    f"📝 Words: {meta.get('word_count', 0)}, 📏 Chars: {meta.get('char_count', 0)}"
                )

        last = segments[-1]
        st.markdown(f"**Last Segment by {last['user']} ({format_timestamp(last['timestamp'])})**")
        st.write(last["text"])

        new_segment = st.text_area("Your Continuation", max_chars=500, height=150, key="new_segment")

        if st.button("➕ Submit Segment"):
            if new_segment.strip():
                segments.append({
                    "text": new_segment.strip(),
                    "timestamp": datetime.now().isoformat(),
                    "user": username.strip(),
                    "coords": [17.3850, 78.4867],
                    "metadata": generate_metadata(new_segment.strip())
                })
                save_stories(stories)
                st.success("✅ Segment added successfully.")
            else:
                st.warning("Please write something before submitting.")

        # Download
        full_story_text = "\n\n".join([seg["text"] for seg in segments])
        st.download_button("📥 Download Story as Text", full_story_text, file_name=f"{selected_title}.txt")

    else:
        st.info("Select a story to continue or start a new one above.")
