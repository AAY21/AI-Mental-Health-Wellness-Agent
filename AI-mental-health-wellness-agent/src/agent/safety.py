import yaml
import re
from pathlib import Path


class SafetyManager:
    def __init__(self, config_path="config/agent.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.crisis_keywords = config["safety"]["crisis_keywords"]
        self.crisis_message = config["safety"]["crisis_response_message"]

    # ---------------------------------------------------------
    # 1. Crisis Detection (High Priority)
    # ---------------------------------------------------------
    def detect_crisis(self, text: str) -> bool:
        """
        Detects if the message indicates danger or self-harm.
        """
        text = text.lower()

        for keyword in self.crisis_keywords:
            if keyword.lower() in text:
                return True

        return False

    # ---------------------------------------------------------
    # 2. Crisis Response
    # ---------------------------------------------------------
    def get_crisis_response(self) -> str:
        """
        Standard crisis response template.
        """
        return self.crisis_message

    # ---------------------------------------------------------
    # 3. Severity Scoring (Optional but useful)
    # ---------------------------------------------------------
    def severity_score(self, text: str) -> int:
        """
        Detect emotional severity using keyword matching.
        Returns score out of 10.
        """
        text = text.lower()

        severity_keywords = {
            "hopeless": 8,
            "worthless": 7,
            "broken": 6,
            "anxious": 5,
            "stressed": 4,
            "sad": 3,
            "tired": 2,
        }

        score = 0
        for keyword, value in severity_keywords.items():
            if keyword in text:
                score = max(score, value)

        return score

    # ---------------------------------------------------------
    # 4. Safe Response Filtering
    # ---------------------------------------------------------
    def sanitize_text(self, text: str) -> str:
        """
        Remove harmful suggestions from AI responses.
        Prevents the agent from outputting unsafe content.
        """
        blocked_patterns = [
            r"kill yourself",
            r"you should hurt",
            r"stop living",
            r"suicide",
        ]

        for pattern in blocked_patterns:
            text = re.sub(pattern, "[removed unsafe content]", text, flags=re.IGNORECASE)

        return text

    # ---------------------------------------------------------
    # 5. Safety Wrapper
    # ---------------------------------------------------------
    def ensure_safe_response(self, ai_text: str) -> str:
        """
        Ensures the model's output is safe before sending to user.
        """
        return self.sanitize_text(ai_text)
