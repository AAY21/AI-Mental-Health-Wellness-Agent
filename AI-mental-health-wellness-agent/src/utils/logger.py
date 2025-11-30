# src/utils/logger.py

"""
Centralized logging utility for the AI Mental Health Agent.
Supports:
- Console logging
- File logging (logs/app.log)
- Auto timestamping
- Log levels (INFO, ERROR, WARNING)
"""

import os
from datetime import datetime


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")


class Logger:

    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)

        # Create log file if not exist
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write("")

    def _write(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_text = f"[{timestamp}] [{level}] {message}"

        # Print to console
        print(log_text)

        # Append to log file
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_text + "\n")

    def info(self, message: str):
        self._write("INFO", message)

    def warning(self, message: str):
        self._write("WARNING", message)

    def error(self, message: str):
        self._write("ERROR", message)


# Global logger instance
logger = Logger()
