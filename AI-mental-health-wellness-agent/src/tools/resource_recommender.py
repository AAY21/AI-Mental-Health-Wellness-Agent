# src/tools/resource_recommender.py

import json
import os

RESOURCES_PATH = "data/resources.json"

# Default resources (auto-created on first run)
DEFAULT_RESOURCES = {
    "stress": [
        {"title": "Deep Breathing Exercise", "link": "https://www.youtube.com/watch?v=UxedG8tEJ6Y"},
        {"title": "5-min Stress Relief Routine", "link": "https://www.youtube.com/watch?v=inpok4MKVLM"},
    ],
    "anxiety": [
        {"title": "Guided Meditation for Anxiety", "link": "https://www.youtube.com/watch?v=O-6f5wQXSu8"},
        {"title": "Anxiety Advice for Students", "link": "https://www.mind.org.uk/information-support/types-of-mental-health-problems/anxiety/about-anxiety/"},
    ],
    "sad": [
        {"title": "Mood Uplifting Playlist", "link": "https://www.youtube.com/watch?v=2OEL4P1Rz04"},
        {"title": "Coping with Feeling Low", "link": "https://www.healthline.com/health/mental-health/things-to-do-when-feeling-down"},
    ],
    "angry": [
        {"title": "Anger Management Tips", "link": "https://www.mentalhealth.org.uk/explore-mental-health/publications/how-manage-and-reduce-stress"},
        {"title": "Progressive Muscle Relaxation", "link": "https://www.youtube.com/watch?v=86HUcX8ZtAk"},
    ],
    "default": [
        {"title": "Student Mental Health Guide", "link": "https://www.unicef.org/parenting/mental-health"},
        {"title": "How to Take Care of Mental Wellbeing", "link": "https://www.nhs.uk/every-mind-matters/"}
    ]
}


def _ensure_resources_file():
    """Creates resources.json if missing."""
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(RESOURCES_PATH):
        with open(RESOURCES_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_RESOURCES, f, indent=4)


def recommend_resources(emotion: str):
    """
    Returns mental-health resources based on detected emotion.
    
    Inputs:
        - emotion: string label (e.g., "stress", "sad", "anxiety")
    
    Output:
        List of resource dicts:
        [
            {"title": "...", "link": "..."},
            ...
        ]
    """

    _ensure_resources_file()

    with open(RESOURCES_PATH, "r", encoding="utf-8") as f:
        resources = json.load(f)

    emotion = emotion.lower().strip()

    if emotion in resources:
        return resources[emotion]

    return resources["default"]
