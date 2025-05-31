from typing import List, Dict, Tuple, Any


SKILL_CATEGORIES = [
    "Python",
    "AI and Machine learning",
    "Git",
    "MongoDB",
    "SQL",
    "Docker",
    "Excel",
    "Javascript",
    "Cloud Platform",
]
LEVEL_WEIGHT = {"Basic": 1.0, "CollegeResearch": 2.0, "Professional": 3.0, "Other": 1.5}


skill2idx: Dict[str, int] = {s: i for i, s in enumerate(SKILL_CATEGORIES)}
