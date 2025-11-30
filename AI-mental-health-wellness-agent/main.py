# main.py

"""
AI Mental Health & Wellness Agent
Entry point for running the ADK Wellness Pipeline.

This script:
- Loads configuration
- Initializes the pipeline
- Runs safety checks
- Processes user messages
- Logs mood analytics
- Returns final agent response
"""

import yaml

from src.agent.safety import SafetyGuard
from src.pipelines.wellness_pipeline import WellnessPipeline
from src.utils.logger import logger
from analytics.logger import analytics_logger


def load_config():
    """Load agent.yaml configuration."""
    try:
        with open("config/agent.yaml", "r") as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise e


def run_agent():
    """
    Entry point for user interaction on CLI.

    Streamlit UI will import and use WellnessPipeline directly,
    but this script allows standalone testing.
    """

    config = load_config()

    safety = SafetyGuard()
    pipeline = WellnessPipeline()

    print("\n🤖 AI Mental Wellness Agent Ready!")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("\nSession ended. Take care! 💚")
            break

        # -----------------------------------------
        # SAFETY CHECK
        # -----------------------------------------
        flagged = safety.check(user_message)

        if flagged["flagged"]:
            print("\n⚠️ SAFETY NOTICE:")
            print(flagged["message"])
            continue

        # -----------------------------------------
        # RUN WELLNESS PIPELINE
        # -----------------------------------------
        logger.info(f"Processing message: {user_message}")

        output = pipeline.run(user_message)

        # -----------------------------------------
        # LOG MOOD FOR ANALYTICS
        # -----------------------------------------
        analytics_logger.log_mood(
            mood=output["mood"]["mood"],
            confidence=output["mood"]["confidence"],
            user_message=user_message
        )

        # -----------------------------------------
        # DISPLAY FINAL AGENT MESSAGE
        # -----------------------------------------
        print("\nAgent:", output["response"])
        print("\n---\n")


if __name__ == "__main__":
    run_agent()
