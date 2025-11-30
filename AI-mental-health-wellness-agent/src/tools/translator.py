# src/tools/translator.py

"""
Lightweight offline Hindi ↔ English translator.
Uses rule-based dictionary mapping to avoid API calls (Kaggle safe).
"""

import re

# Basic dictionary for emotional & conversational words
HI_TO_EN = {
    "मुझे": "I",
    "डर": "fear",
    "लग रहा": "feeling",
    "है": "am",
    "चिंता": "anxiety",
    "हो रही": "having",
    "थक": "tired",
    "गया": "exhausted",
    "उदास": "sad",
    "खुश": "happy",
    "बहुत": "very",
    "ज़्यादा": "too much",
    "नहीं": "not",
    "ठीक": "okay",
    "सकता": "can",
    "सकती": "can",
    "मदद": "help",
    "चाहिए": "needed",
    "क्यों": "why",
    "मैं": "I",
    "परेशान": "upset",
}

EN_TO_HI = {
    "sad": "उदास",
    "anxiety": "चिंता",
    "stress": "तनाव",
    "angry": "गुस्सा",
    "happy": "खुश",
    "tired": "थका हुआ",
    "I am": "मैं",
    "feeling": "महसूस कर रहा हूँ",
    "help": "मदद",
    "need": "ज़रूरत है",
    "okay": "ठीक",
    "not": "नहीं",
    "very": "बहुत",
}


def _replace_words(text, dictionary):
    """Simple dictionary-based replace."""
    for hi, en in dictionary.items():
        text = re.sub(rf"\b{hi}\b", en, text, flags=re.IGNORECASE)
    return text


def translate_to_english(text: str) -> str:
    """
    Hindi → English translation (rule-based).
    """
    translated = _replace_words(text, HI_TO_EN)
    return translated


def translate_to_hindi(text: str) -> str:
    """
    English → Hindi translation (rule-based).
    """
    translated = _replace_words(text, EN_TO_HI)
    return translated
