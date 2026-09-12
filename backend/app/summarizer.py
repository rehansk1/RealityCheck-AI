from transformers import pipeline
from app.config import SUMMARIZER_MODEL


print("Loading Summarization Model...")


summarizer = pipeline(
    "text2text-generation",
    model=SUMMARIZER_MODEL
)


print("Summarization Model Loaded Successfully!")


def summarize_text(text):

    result = summarizer(
        f"summarize: {text}",
        max_new_tokens=80,
        min_length=20,
        do_sample=False
    )

    return result[0]["generated_text"]