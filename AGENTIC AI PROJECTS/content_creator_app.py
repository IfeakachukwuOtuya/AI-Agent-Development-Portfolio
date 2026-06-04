import streamlit as st
import os
from crewai import Agent, Task, Crew
from utils import get_openai_api_key

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Agentic AI – YouTube Shorts Micro-History Creator",
    page_icon="🎥",
    layout="centered"
)

# -----------------------------
# Custom CSS for Background + Style
# -----------------------------
page_bg = """
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #232526 100%);
    color: #f5f5f5;
}

/* Title styling */
.big-title {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    text-align: center;
    color: #ffffff;
    padding-top: 10px;
    letter-spacing: 1px;
}

/* Subtitle styling */
.sub-title {
    font-size: 1.2rem;
    text-align: center;
    color: #cccccc;
    margin-top: -10px;
    padding-bottom: 20px;
}

/* Section header */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #00d4ff;
    margin-top: 20px;
    padding-bottom: 5px;
}

/* Input box styling */
input {
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Card container */
.result-card {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
    box-shadow: 0 0 12px rgba(0,0,0,0.35);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# App Title & Intro
# -----------------------------
st.markdown('<div class="big-title">🎥 Agentic AI: Shorts Micro-History Creator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate irresistible, curiosity-driven YouTube Shorts ideas instantly</div>', unsafe_allow_html=True)

# -----------------------------
# API Key Setup
# -----------------------------
os.environ["CREWAI_TESTING"] = "true"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# -----------------------------
# Agent Definition
# -----------------------------
creator_agent = Agent(
    name="YouTube Shorts Micro-History Strategist",
    role="YouTube Shorts Micro-History Strategist",
    goal="Plan high-retention YouTube Shorts about surprising origins",
    backstory=(
        "You specialize in 30–45 second micro-history stories with fast hooks, plot twists, and "
        "simple visuals that any solo creator can film at home. You excel at viral content strategy."
    ),
    llm="gpt-4o",
    verbose=True,
)

# -----------------------------
# User Input Section
# -----------------------------
st.markdown('<div class="section-header">🔍 What topic do you want a Short about?</div>', unsafe_allow_html=True)

topic = st.text_input(
    "Example: 'Why pencils are yellow', 'Origin of bubble wrap', 'Why microwaves beep'",
    placeholder="Enter an everyday object, invention, habit, or trend..."
)

generate_btn = st.button("✨ Generate Video Blueprint")

# -----------------------------
# Content Generation Logic
# -----------------------------
def generate_short_blueprint(topic: str):
    task = Task(
        description=(
            "Create a YouTube Shorts video blueprint in a JSON dictionary. "
            "Platform: YouTube Shorts (30–45 seconds, vertical). "
            f"Topic: {topic}. "
            "Focus on hooks, clarity, searchable titles, and simple at-home visual ideas."
        ),
        expected_output=(
            '''
            {
                "videos": [
                    {
                        "title": "<title>",
                        "hook_main": "<12-word hook>",
                        "hook_alt": "<alt hook>",
                        "visuals": ["simple prop or b-roll idea 1", "idea 2"],
                        "tags": ["#microhistory", "#everydaythings", "#shorts"],
                        "cta": "<comment question>"
                    }
                ]
            }
            '''
        ),
        agent=creator_agent,
        output_type="string"
    )

    crew = Crew(
        agents=[creator_agent],
        tasks=[task],
        verbose=False,
    )

    return crew.kickoff()

# -----------------------------
# Output Display
# -----------------------------
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("⏳ Generating your micro-history Short blueprint..."):
            result = generate_short_blueprint(topic)

        st.success("🚀 Blueprint Ready!")

        st.markdown('<div class="section-header">📋 Your YouTube Short Blueprint</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.code(str(result), language="json")
        st.markdown('</div>', unsafe_allow_html=True)
