# analytics/logger.py

"""
Analytics Logger
----------------
Stores user mood logs for:
- Weekly emotional trend charts
- Real-time dashboard analytics
- Tracking frequency of different moods

Logs are appended to data/emotion_logs.csv
Structure:
timestamp, mood, confidence, user_message
"""

import os
import csv
from datetime import datetime


DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "emotion_logs.csv")


class AnalyticsLogger:

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        # Initialize CSV with headers if missing
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "mood", "confidence", "user_message"])

    def log_mood(self, mood: str, confidence: float, user_message: str):
        """Append mood analysis entry to CSV."""
        timestamp = datetime.utcnow().isoformat()

        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, mood, confidence, user_message])

    def load_logs(self):
        """Load logs as list of dicts."""
        logs = []

        if not os.path.exists(LOG_FILE):
            return logs

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)

        return logs


# Global instance
analytics_logger = AnalyticsLogger()
