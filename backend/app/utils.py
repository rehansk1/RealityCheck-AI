import re
from pathlib import Path


def clean_text(text: str) -> str:
    """
    Clean article text by removing extra spaces and line breaks.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if uploaded file has an allowed extension.
    """
    extension = Path(filename).suffix.lower()
    return extension in allowed_extensions


def truncate_text(text: str, max_length: int = 4000) -> str:
    """
    Limit text length before sending to the AI model.
    """
    if len(text) <= max_length:
        return text

    return text[:max_length]


def round_confidence(score: float) -> float:
    """
    Convert confidence score to percentage.
    """
    return round(score * 100, 2)