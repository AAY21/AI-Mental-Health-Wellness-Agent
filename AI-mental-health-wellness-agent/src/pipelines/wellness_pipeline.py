# src/pipelines/wellness_pipeline.py

"""
Wellness Pipeline for ADK Mental Health Agent.

Pipeline responsibilities:
- Receive user input request
- Apply safety checks
- Detect emotion
- Run orchestrator (LLM Response Engine)
- Log emotional data for dashboard
- Prepare final structured response

This file acts as a bridge between:
ADK Agent <--> Tools <--> Orchestrator <--> Analytics
"""

from agent.orchestrator import MentalHealthAgent
from analytics.trend_tracker import log_emotion
from agent.safety import check_safety


class WellnessPipeline:
    """
    Combines the entire agent workflow in a single pipeline.

    Entry point: pipeline.run(user_text, lang="en")
    """

    def __init__(self, llm):
        # Orchestrator is the core AI engine
        self.orchestrator = MentalHealthAgent(llm)

    def run(self, user_text: str, lang="en"):
        """
        Executes the full wellness pipeline.

        Returns:
            {
                "response": "...",
                "emotion": "...",
                "intensity": ...,
                "suggestions": [...],
                "translated": "...",
                "safe": True/False
            }
        """

        # 1. Primary safety check
        safety_flag = check_safety(user_text)
        if not safety_flag:
            return {
                "response": "I’m really concerned about your wellbeing. Please reach out to a trusted adult, counselor, or local mental health helpline immediately.",
                "emotion": "critical",
                "intensity": 10,
                "suggestions": [],
                "translated": None,
                "safe": False
            }

        # 2. Run the mental health agent orchestrator
        agent_output = self.orchestrator.generate(user_text, lang=lang)

        # 3. Log emotion for dashboard trend graph
        log_emotion(
            emotion=agent_output["emotion"],
            intensity=agent_output["intensity"]
        )

        # 4. Final structured output for Streamlit/Kaggle
        return {
            "response": agent_output["response"],
            "emotion": agent_output["emotion"],
            "intensity": agent_output["intensity"],
            "suggestions": agent_output["suggestions"],
            "translated": agent_output["translated"],
            "safe": True
        }

    # Pipeline helper: Journal entry route
    def add_journal(self, text: str):
        return self.orchestrator.add_journal(text)

    # Pipeline helper: Mental health resource route
    def get_resources(self, emotion: str):
        return self.orchestrator.get_resources(emotion)
