import streamlit as st
import json
import os
import uuid
from datetime import datetime

# Constants
STORY_FILE = "storage/stories.json"
os.makedirs("storage", exist_ok=True)

# Load existing stories or create empty structure
def load_stories():
    if os.path.exists(STORY_FILE):
        with open(STORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass
    return {}

# Save stories to file
def save_stories(stories):
    with open(STORY_FILE, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)

# Initialize session state
if "stories" not in st.session_state:
    st.session_state.stories = load_stories()

st.set_page_config(page_title="Sahakathanam", layout="wide")
st.sidebar.title("📖 సహకథనం (Sahakathanam)")
st.sidebar.markdown("A Collaborative Storytelling Platform")

# Sidebar inputs
language = st.sidebar.selectbox("Language", ["Telugu", "Hindi", "Kannada", "Tamil", "Malayalam"])
username = st.sidebar.text_input("Your Name", value="anon")

# Suggested story titles
hot_titles = {
    "Telugu": ["రామాయణ కథ", "తెనాలి రామకృష్ణ కథ", "బిర్బల్ కథలు"],
    "Hindi": ["रामायण कथा", "तेनालीराम की कहानी", "अकबर-बीरबल"]
}

st.title("Collaborative Storytelling in Indian Languages")

# Tabs for Create and Continue
tab1, tab2 = st.tabs(["Start a New Story", "Continue Existing Story"])

with tab1:
    st.subheader("Start a New Story")

    if language in hot_titles:
        st.markdown("Suggested Titles:")
        for t in hot_titles[language]:
            st.markdown(f"- {t}")

    title = st.text_input("Story Title")
    initial_text = st.text_area("Opening Lines (2-3 sentences)", max_chars=500)

    if st.button("Submit New Story"):
        if title and initial_text:
            story_id = str(uuid.uuid4())
            st.session_state.stories[story_id] = {
                "title": title,
                "language": language,
                "segments": [
                    {
                        "text": initial_text,
                        "timestamp": datetime.now().isoformat(),
                        "user": username,
                        "coords": [17.3850, 78.4867]  # Sample location
                    }
                ]
            }
            save_stories(st.session_state.stories)
            st.success("Story created successfully.")
        else:
            st.warning("Please provide both a title and the initial text.")

with tab2:
    st.subheader("Continue a Story")
    stories = st.session_state.stories
    options = {v["title"]: k for k, v in stories.items() if v.get("language") == language}
    selected_title = st.selectbox("Choose a story to continue", ["--"] + list(options.keys()))

    if selected_title != "--":
        story_id = options[selected_title]
        selected_story = stories[story_id]
        last_segment = selected_story["segments"][-1]["text"]
        st.markdown("Last Segment:")
        st.write(last_segment)

        new_segment = st.text_area("Your Continuation", max_chars=500)

        if st.button("Submit Segment"):
            if new_segment:
                selected_story["segments"].append({
                    "text": new_segment,
                    "timestamp": datetime.now().isoformat(),
                    "user": username,
                    "coords": [17.3850, 78.4867]  # Sample location
                })
                save_stories(stories)
                st.success("Segment added.")
            else:
                st.warning("Please write something before submitting.")
    else:
        st.info("Start a new story or select one to continue.")
