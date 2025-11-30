# src/agent/memory.py

import time
from collections import deque


class ConversationMemory:
    """
    Lightweight memory system:
    - Stores last N messages
    - Used for conversational context
    - Also logs emotional signals for analytics
    """

    def __init__(self, max_messages=20):
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)

    def add(self, role, content):
        """Add a message to memory."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })

    def get_context(self):
        """Return recent conversation context as a clean list."""
        return list(self.messages)

    def clear(self):
        """Clear memory."""
        self.messages.clear()


class EmotionMemory:
    """
    Stores emotional logs for:
    - trend analysis
    - weekly charts
    - dashboard analytics
    """

    def __init__(self):
        self.logs = []  # in-memory list; CSV will be handled separately

    def record(self, emotion, intensity):
        """Record an emotional snapshot."""
        self.logs.append({
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": time.time()
        })

    def get_recent(self, limit=30):
        """Return recent emotional entries."""
        return self.logs[-limit:]

    def get_all(self):
        """Return complete emotional history."""
        return self.logs


# GLOBAL SINGLETON-LIKE HELPERS
conversation_memory = ConversationMemory()
emotion_memory = EmotionMemory()
