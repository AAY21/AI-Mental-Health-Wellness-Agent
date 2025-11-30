# src/tools/journal_tool.py

import os
from datetime import datetime

JOURNAL_PATH = "data/journal_entries.txt"


def store_journal_entry(text: str):
    """
    Saves a student's journal entry with timestamp.
    Creates the file if not present.

    Returns:
        {
            "status": "saved",
            "timestamp": "...",
            "length": ...
        }
    """

    os.makedirs("data", exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    entry = f"\n[{timestamp}]\n{text}\n{'-'*50}\n"

    with open(JOURNAL_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    return {
        "status": "saved",
        "timestamp": timestamp,
        "length": len(text)
    }


def read_journal_entries(limit: int = 5):
    """
    Returns the most recent N journal entries.
    """

    if not os.path.exists(JOURNAL_PATH):
        return []

    with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return []

    # Split entries by separator line
    entries = content.split("------------------------------------------")
    entries = [e.strip() for e in entries if e.strip()]

    return entries[-limit:]
