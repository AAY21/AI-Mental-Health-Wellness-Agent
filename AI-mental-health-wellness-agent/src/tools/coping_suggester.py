# src/tools/coping_suggester.py

"""
Coping Suggestions Tool
-----------------------
Based on the detected mood, this tool provides:
- Personalized coping activities
- Breathing exercises
- Small actionable micro-steps
- Student-friendly guidance
"""

import json
import random
from typing import List


class CopingSuggester:
    def __init__(self, activities_file="data/activities.json"):
        with open(activities_file, "r") as f:
            self.activities = json.load(f)

    def suggest(self, mood: str, count: int = 3) -> List[str]:
        mood = mood.lower().strip()

        if mood not in self.activities:
            return [
                "Try a short breathing exercise (inhale 4s, hold 2s, exhale 6s).",
                "Drink some water and stretch your body for 30 seconds.",
                "Write down what you're feeling in a small journal entry."
            ]

        suggestions = self.activities[mood]

        if len(suggestions) <= count:
            return suggestions

        # Random multiple suggestions (always fresh)
        return random.sample(suggestions, count)
