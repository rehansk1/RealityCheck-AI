from app.summarizer import summarize_text


def create_summary(text: str):
    """
    Generate article summary.
    """

    summary = summarize_text(text)

    return summary