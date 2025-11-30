# src/tools/mood_detector.py

"""
Mood Detector Tool
------------------
Uses an LLM (via ADK runtime) to classify the emotional tone of a student's text.
Produces a structured JSON containing:
- mood label
- confidence score
- short reasoning
"""

from adk import tool


@tool()
def detect_mood(user_input: str) -> dict:
    """
    Detects the emotional tone of the user's message.

    Args:
        user_input (str): The message provided by the student.

    Returns:
        dict: {
            "mood": <emotion_label>,
            "confidence": <0-1>,
            "reason": <short explanation>
        }
    """

    prompt = f"""
    You are an expert psychologist and emotional analysis system.
    Analyze the text below and classify the student's emotional state.

    TEXT:
    "{user_input}"

    Respond ONLY in JSON with the schema:
    {{
        "mood": "<one of: happy, sad, stressed, anxious, angry, neutral>",
        "confidence": <0-1 float>,
        "reason": "<very short explanation>"
    }}
    """

    # ADK internal LLM call
    result = detect_mood.llm(prompt)

    return result
