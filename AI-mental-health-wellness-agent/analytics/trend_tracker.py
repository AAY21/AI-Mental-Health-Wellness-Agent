# analytics/trend_tracker.py

"""
Trend Tracker
-------------
Reads from emotion_logs.csv and produces:

- Weekly emotion trends
- Count of each emotion
- Daily emotional timeline
- Trend data for Streamlit charts

Used by the real-time dashboard in streamlit_app/app.py
"""

import os
import pandas as pd
from datetime import datetime, timedelta


LOG_FILE = os.path.join("data", "emotion_logs.csv")


class TrendTracker:

    def __init__(self):
        pass

    def _load_df(self):
        """Load CSV as DataFrame, create if missing."""
        if not os.path.exists(LOG_FILE):
            return pd.DataFrame(columns=["timestamp", "mood", "confidence", "user_message"])

        df = pd.read_csv(LOG_FILE)

        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    # -----------------------------------------------------------
    # Weekly Mood Frequency (Bar Chart)
    # -----------------------------------------------------------
    def weekly_mood_counts(self):
        df = self._load_df()
        if df.empty:
            return {}

        one_week_ago = datetime.utcnow() - timedelta(days=7)
        recent = df[df["timestamp"] >= one_week_ago]

        if recent.empty:
            return {}

        return recent["mood"].value_counts().to_dict()

    # -----------------------------------------------------------
    # Daily Mood Trend (Line Chart)
    # -----------------------------------------------------------
    def daily_trend(self):
        df = self._load_df()
        if df.empty:
            return {}

        df["date"] = df["timestamp"].dt.date
        trend = df.groupby("date")["mood"].agg(list).to_dict()
        return trend

    # -----------------------------------------------------------
    # Most Frequent Mood of the Week
    # -----------------------------------------------------------
    def dominant_weekly_mood(self):
        counts = self.weekly_mood_counts()
        if not counts:
            return None
        return max(counts, key=counts.get)

    # -----------------------------------------------------------
    # Mood Confidence Average
    # -----------------------------------------------------------
    def average_confidence(self):
        df = self._load_df()
        if df.empty:
            return 0
        return float(df["confidence"].mean())

    # -----------------------------------------------------------
    # Usage stats (for dashboard)
    # -----------------------------------------------------------
    def usage_stats(self):
        df = self._load_df()
        if df.empty:
            return {
                "total_entries": 0,
                "unique_days": 0
            }

        unique_days = df["timestamp"].dt.date.nunique()

        return {
            "total_entries": len(df),
            "unique_days": unique_days
        }


# Global instance
trend_tracker = TrendTracker()
