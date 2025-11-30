# src/utils/validators.py

"""
Validation utilities for user input, mood labels,
and structured data objects passed through the Wellness Agent pipeline.
"""

VALID_MOODS = [
    "happy", "sad", "stressed", "anxious", "angry", "neutral"
]


def validate_user_input(text: str) -> bool:
    """
    Ensures the user message is safe and non-empty.

    Returns:
        True if valid, False otherwise.
    """
    if not text:
        return False
    if len(text.strip()) == 0:
        return False
    if len(text) > 2000:
        return False
    return True


def validate_mood_label(mood: str) -> bool:
    """
    Ensures mood label is one of the supported categories.
    """
    if not isinstance(mood, str):
        return False
    return mood.lower() in VALID_MOODS


def validate_journal_entry(text: str) -> bool:
    """
    Ensures journal entries are meaningful and not empty.
    """
    if not text or len(text.strip()) < 5:
        return False
    return True


def validate_json_structure(data: dict, required_keys: list) -> bool:
    """
    Ensures JSON returned by tools follows required schema.

    Args:
        data (dict): JSON object to validate.
        required_keys (list): Mandatory fields.

    Returns:
        bool
    """
    if not isinstance(data, dict):
        return False

    return all(key in data for key in required_keys)
