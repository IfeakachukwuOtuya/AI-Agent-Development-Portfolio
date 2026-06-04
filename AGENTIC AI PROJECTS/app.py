import streamlit as st
import os
import json
import re
from crewai import Agent, Task, Crew
from utils import get_openai_api_key

# -----------------------------
# Page config + background
# -----------------------------
st.set_page_config(page_title="Agentic AI – YouTube Shorts Demo", page_icon="🎥", layout="centered")
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(135deg,#081826 0%, #0e1720 50%, #111827 100%);
    color: #e6eef6;
}
.big-title { font-size:2.4rem; font-weight:800; text-align:center; margin-top:6px }
.sub-title { color:#bcd; text-align:center; margin-top:-6px; margin-bottom:18px }
.card { background:rgba(255,255,255,0.03); padding:18px; border-radius:12px; box-shadow:0 6px 24px rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.04); margin-bottom:12px }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎥 Agentic AI – YouTube Shorts Micro-History</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Type a topic and instantly generate 5 micro-history video blueprints</div>', unsafe_allow_html=True)

# -----------------------------
# API key
# -----------------------------
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["CREWAI_TESTING"] = "true"

# -----------------------------
# User input
# -----------------------------
topic = st.text_input("Enter a topic (object, habit, invention, trend)", placeholder="e.g. Why pencils are yellow")
generate_btn = st.button("✨ Generate 5 Video Blueprints")

# -----------------------------
# CrewAI Agent
# -----------------------------
creator_agent = Agent(
    name="YouTube Shorts Micro-History Strategist",
    role="YouTube Shorts Micro-History Strategist",
    goal="Plan a 1-week slate of high-retention YouTube Shorts about surprising origins",
    backstory=(
        "You specialize in 30-45s micro-history that hooks fast, pays off with a twist. "
        "Ideas must be filmable by a solo creator at home with minimal props."
    ),
    llm="gpt-4o",
    verbose=False,
)

# -----------------------------
# Generate 5 blueprints
# -----------------------------
def generate_blueprints(topic, n=5):
    task = Task(
        description=(
            f"Create {n} unique YouTube Shorts blueprints (vertical 9:16, 30-45s). "
            f"Topic: {topic}. Each blueprint must include title, hook_main (<=12 words), hook_alt, "
            "visuals (2 ideas), tags (3-6 hashtags), cta (comment question). "
            "Return ONLY valid JSON exactly as an array under the key 'videos'. Do NOT include any extra text or explanation."
        ),
        expected_output=json.dumps({"videos":[{} for _ in range(n)]}),
        agent=creator_agent,
        output_type="string"
    )

    crew = Crew(agents=[creator_agent], tasks=[task])
    result = crew.kickoff()

    # Robust JSON parsing with fallback
    try:
        parsed = json.loads(result.raw)
    except:
        m = re.search(r"\{.*\}", result.raw, re.S)
        if m:
            parsed = json.loads(m.group(0))
        else:
            parsed = {"videos":[{"title":"Error generating video", "hook_main":"","hook_alt":"","visuals":[],"tags":[],"cta":""} for _ in range(n)]}

    videos = parsed.get("videos", [])
    if len(videos) < n:
        for i in range(len(videos), n):
            videos.append({"title":f"Extra Idea {i+1}", "hook_main":"","hook_alt":"","visuals":[],"tags":[],"cta":""})
    elif len(videos) > n:
        videos = videos[:n]

    return videos

# -----------------------------
# Display results
# -----------------------------
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner(f"⏳ Generating 5 micro-history Shorts for '{topic}'..."):
            videos = generate_blueprints(topic)
        
        for idx, v in enumerate(videos, start=1):
            st.markdown(f'''
            <div class="card">
            <b>{idx}. {v.get("title","(no title)")}</b><br>
            Hook: {v.get("hook_main","")}<br>
            Alt Hook: {v.get("hook_alt","")}<br>
            Visuals: {", ".join(v.get("visuals",[]))}<br>
            Tags: {", ".join(v.get("tags",[]))}<br>
            CTA: {v.get("cta","")}
            </div>
            ''', unsafe_allow_html=True)
