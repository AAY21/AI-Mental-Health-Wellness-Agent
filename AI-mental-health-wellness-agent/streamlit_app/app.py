# streamlit_app/app.py
"""
Streamlit UI for AI Mental Health & Wellness Agent (Student-focused)

Features:
- Chat UI (English / Hindi)
- Shows agent response, suggestions, and translation
- Save journal entries (calls pipeline.add_journal)
- Shows weekly emotional trend chart (reads data/emotion_logs.csv)
- Shows recent journal entries (reads data/journal_entries.txt)

This app attempts to import your project pipeline:
    from src.pipelines.wellness_pipeline import WellnessPipeline
If unavailable, a lightweight fallback pipeline is used so you can iterate locally.

Author: Generated to fit ai-mental-health-agent project structure
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- Try to import your real pipeline (preferred) ----------
try:
    from src.pipelines.wellness_pipeline import WellnessPipeline
    from src.tools.journal_tool import read_journal_entries
    REAL_PIPELINE_AVAILABLE = True
except Exception as e:
    # If your project modules aren't on PYTHONPATH or not yet created,
    # provide a minimal fallback pipeline for UI testing.
    REAL_PIPELINE_AVAILABLE = False

    # fallback journal reader
    def read_journal_entries(limit=5):
        path = "data/journal_entries.txt"
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            return []
        entries = [e.strip() for e in content.split("------------------------------------------") if e.strip()]
        return entries[-limit:]

    # minimal fallback llm function
    def _fallback_llm(prompt: str) -> str:
        # Simple, safe reply: reflect and offer small coping tips
        reply = "Thanks for sharing. I hear you. Try taking 5 deep breaths now."
        return reply

    class WellnessPipeline:
        def __init__(self, llm=None):
            self.llm = llm or _fallback_llm

        def run(self, user_text: str, lang="en"):
            # very small heuristics mimic your tools
            text = user_text.lower()
            if any(k in text for k in ["suicide", "kill myself", "want to die"]):
                return {
                    "response": "It seems you may be in danger. Please contact emergency services or a helpline immediately.",
                    "emotion": "critical",
                    "intensity": 10,
                    "suggestions": [],
                    "translated": None,
                    "safe": False
                }
            # quick mood detector
            if any(k in text for k in ["exam", "exam tomorrow", "deadline", "pressure"]):
                emotion = "stress"
                intensity = 4
                suggestions = ["Short walk", "Pomodoro 25/5"]
            elif any(k in text for k in ["panic", "panic attack", "panic mode", "can't sleep", "cant sleep"]):
                emotion = "anxiety"
                intensity = 5
                suggestions = ["5-min breathing", "Grounding exercise"]
            elif any(k in text for k in ["sad", "alone", "depressed", "low"]):
                emotion = "sad"
                intensity = 3
                suggestions = ["Talk to a friend", "Write 3 things you're grateful for"]
            else:
                emotion = "neutral"
                intensity = 1
                suggestions = ["Take a short break", "Hydrate"]

            response = self.llm(user_text)
            return {
                "response": response,
                "emotion": emotion,
                "intensity": intensity,
                "suggestions": suggestions,
                "translated": None if lang == "en" else response,
                "safe": True
            }

        def add_journal(self, text: str):
            # write to file
            os.makedirs("data", exist_ok=True)
            path = "data/journal_entries.txt"
            ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            entry = f"\n[{ts}]\n{text}\n{'-'*50}\n"
            with open(path, "a", encoding="utf-8") as f:
                f.write(entry)
            return {"status": "saved", "timestamp": ts}

        def get_resources(self, emotion: str):
            # tiny static mapping
            mapping = {
                "stress": [{"title": "Pomodoro Guide", "link": "https://todoist.com/productivity-methods/pomodoro-technique"}],
                "anxiety": [{"title": "Grounding Technique", "link": "https://www.youtube.com/watch?v=GiUDZtzRB-Q"}],
                "sad": [{"title": "Coping with Feeling Low", "link": "https://www.healthline.com"}],
                "neutral": [{"title": "Mental Wellbeing Tips", "link": "https://www.nhs.uk/every-mind-matters/"}]
            }
            return mapping.get(emotion, mapping["neutral"])



# ---------- Initialize pipeline ----------
if REAL_PIPELINE_AVAILABLE:
    # You may want to pass a real LLM callable here (ADK LLM or a wrapper)
    # For local dev this will use the fallback llm unless you wire one up.
    pipeline = WellnessPipeline(llm=None)
else:
    pipeline = WellnessPipeline()

# ---------- Streamlit UI Layout ----------
st.set_page_config(page_title="AI Student Wellness Agent", layout="wide")
st.title("🌿 AI Student Mental Health & Wellness Assistant")

# Left column: Chat & Interaction
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Chat with the Agent")
    language = st.selectbox("Language", ("English", "Hindi"))

    user_input = st.text_area("How are you feeling? Share as much as you'd like.", height=120)

    submit_col, journal_col = st.columns([1,1])
    with submit_col:
        submit = st.button("Send")
    with journal_col:
        save_journal = st.button("Save as Journal Entry")

    # Handle submit
    if submit and user_input and user_input.strip():
        lang_code = "hi" if language.lower().startswith("h") else "en"
        with st.spinner("Analyzing..."):
            output = pipeline.run(user_input, lang=lang_code)

        # Display response
        if not output.get("safe", True):
            st.error(output["response"])
        else:
            st.success(output["response"])

            # suggestions panel
            st.markdown("**Suggestions**")
            for s in output.get("suggestions", []):
                st.write(f"- {s}")

            # resources
            st.markdown("**Recommended resources**")
            try:
                resources = pipeline.get_resources(output.get("emotion", "neutral"))
                for r in resources:
                    st.write(f"- [{r.get('title')}]({r.get('link')})")
            except Exception:
                # pipeline may not implement get_resources
                pass

            # translation (if available)
            if output.get("translated"):
                st.markdown("**Translated**")
                st.write(output["translated"])

    # Handle saving journal entry
    if save_journal and user_input and user_input.strip():
        res = pipeline.add_journal(user_input)
        if res.get("status") == "saved":
            st.success(f"Journal saved at {res.get('timestamp')}")
        else:
            st.info("Journal saved.")

    # Quick example prompts
    st.markdown("---")
    st.markdown("**Try these examples:**")
    st.write("- I have an exam tomorrow and can't sleep.")
    st.write("- I'm feeling very anxious about presentations.")
    st.write("- I want to talk about how lonely I feel.")

with col2:
    st.header("Dashboard & Trends")

    # Emotion trend chart (reads data/emotion_logs.csv or fallback to pipeline logs)
    st.subheader("Weekly Emotion Trend")

    # Attempt to load CSV logs (preferred)
    logs_path = "data/emotion_logs.csv"
    df_trend = None
    if os.path.exists(logs_path):
        try:
            df_trend = pd.read_csv(logs_path, parse_dates=[0], header=None)
            # expected format: timestamp, message, mood
            if df_trend.shape[1] >= 3:
                df_trend = df_trend.iloc[:, :3]
                df_trend.columns = ["timestamp", "message", "mood"]
                df_trend["timestamp"] = pd.to_datetime(df_trend["timestamp"], errors="coerce")
                # aggregate per day
                df_trend["date"] = df_trend["timestamp"].dt.date
                counts = df_trend.groupby(["date", "mood"]).size().unstack(fill_value=0)
                st.line_chart(counts)
            else:
                st.info("emotion_logs.csv exists but is using an unexpected format.")
        except Exception as e:
            st.error("Unable to read emotion logs: " + str(e))
    else:
        # Try to build plot from pipeline/emotion memory if accessible
        try:
            # If analytics/trend_tracker created a CSV at data/emotion_logs.csv this will show it.
            st.info("No emotion log CSV found. Interact with the agent to build logs.")
        except Exception:
            st.info("No emotion logs available yet.")

    st.markdown("---")
    st.subheader("Recent Journal Entries")
    entries = read_journal_entries(limit=5)
    if entries:
        for i, e in enumerate(reversed(entries), 1):
            st.markdown(f"**Entry {i}**")
            st.text(e.strip())
    else:
        st.info("No journal entries yet. Use 'Save as Journal Entry' in the chat panel to add one.")

    st.markdown("---")
    st.subheader("Quick Links & Safety")
    st.write("- If in danger, contact your local emergency services immediately.")
    st.write("- India Crisis Helpline: 9152987821")
    st.write("- International helplines: https://www.befrienders.org/")

# ---------- Footer ----------
st.markdown("---")
st.caption("This UI is a demo interface for the ADK Mental Health Agent. For critical situations, always contact a professional.")
