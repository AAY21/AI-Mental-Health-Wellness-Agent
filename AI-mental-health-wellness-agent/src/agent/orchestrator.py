import time
from src.agent.safety import SafetyGuard
from src.agent.memory import MemoryManager
from src.agent.prompts import PROMPT_MOOD_ANALYSIS, PROMPT_CONVERSATION
from src.tools.mood_detector import MoodDetector
from src.tools.coping_suggester import CopingSuggester
from src.tools.journal_tool import JournalTool
from src.tools.resource_recommender import ResourceRecommender
from src.tools.translator import Translator


class WellnessOrchestrator:

    def __init__(self):
        self.memory = MemoryManager()
        self.safety = SafetyGuard()
        self.mood_detector = MoodDetector()
        self.coping = CopingSuggester()
        self.journal = JournalTool()
        self.recommender = ResourceRecommender()
        self.translator = Translator()

    def process(self, user_text: str, lang="en"):
        # Safety check
        flagged = self.safety.check(user_text)
        if flagged:
            return flagged

        # Mood detection
        mood = self.mood_detector.detect(user_text)
        self.memory.store_emotion(mood)

        # Get 3 coping suggestions
        coping_list = self.coping.suggest(mood)

        # Format list
        formatted = "\n".join([f"• {x}" for x in coping_list])

        # Journal log
        self.journal.save_entry(user_text, mood)

        # Resource suggestions
        resources = self.recommender.recommend(mood)
        resources_fmt = "\n".join([f"• {r}" for r in resources])

        reply = (
            f"You're feeling **{mood}**.\n\n"
            f"Here are some helpful strategies:\n{formatted}\n\n"
            f"Helpful resources:\n{resources_fmt}"
        )

        # Translation if needed
        if lang == "hi":
            reply = self.translator.to_hindi(reply)

        return reply
