from transformers import pipeline


# ============================================================
# MODEL SETTINGS
# ============================================================

MODEL_NAME = "capcheck/ai-image-detection"

# Your classification rule:
# REAL score > 50%  -> REAL
# REAL score <= 50% -> FAKE

REAL_THRESHOLD = 50.0


# ============================================================
# LOAD AI IMAGE DETECTION MODEL
# ============================================================

print("Loading AI image detection model...")

detector = pipeline(
    "image-classification",
    model=MODEL_NAME
)

print("AI image detection model loaded successfully.")


# ============================================================
# DETECT AI IMAGE
# ============================================================

def detect_ai(image):
    """
    Analyze an image and classify it as REAL or FAKE.

    Rule:
        REAL score > 50%  -> REAL
        REAL score <= 50% -> FAKE
    """

    # --------------------------------------------------------
    # RUN MODEL
    # --------------------------------------------------------

    results = detector(image)

    if not results:
        raise ValueError(
            "The AI image detection model returned no result."
        )


    # --------------------------------------------------------
    # FIND REAL AND FAKE SCORES
    # --------------------------------------------------------

    real_score = 0.0
    fake_score = 0.0

    for item in results:

        label = str(
            item.get("label", "")
        ).upper().strip()

        score = float(
            item.get("score", 0)
        )

        if label == "REAL":
            real_score = score

        elif label == "FAKE":
            fake_score = score


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if real_score == 0 and fake_score == 0:

        raise ValueError(
            "Could not determine REAL or FAKE score."
        )


    # --------------------------------------------------------
    # CONVERT TO PERCENTAGE
    # --------------------------------------------------------

    real_percentage = round(
        real_score * 100,
        2
    )

    fake_percentage = round(
        fake_score * 100,
        2
    )


    # --------------------------------------------------------
    # YOUR CLASSIFICATION RULE
    # --------------------------------------------------------

    if real_percentage > REAL_THRESHOLD:

        prediction = "REAL"

        summary = (
            f"The image received a real-image score of "
            f"{real_percentage:.2f}%. Because this score "
            f"is above the {REAL_THRESHOLD:.1f}% threshold, "
            f"the image is classified as REAL."
        )

        reason = (
            f"The real-image score of {real_percentage:.2f}% "
            f"is greater than the {REAL_THRESHOLD:.1f}% "
            f"threshold."
        )

    else:

        prediction = "FAKE"

        summary = (
            f"The image received a real-image score of "
            f"{real_percentage:.2f}%. Because this score "
            f"is {REAL_THRESHOLD:.1f}% or below, "
            f"the image is classified as FAKE."
        )

        reason = (
            f"The real-image score of {real_percentage:.2f}% "
            f"is {REAL_THRESHOLD:.1f}% or below."
        )


    # --------------------------------------------------------
    # RETURN COMPLETE RESULT
    # --------------------------------------------------------

    return {

        "prediction": prediction,

        # This is the score used for your 50% rule.
        "confidence": real_percentage,

        # Extra model information.
        "real_score": real_percentage,

        "fake_score": fake_percentage,

        # Threshold used.
        "threshold": REAL_THRESHOLD,

        # Human-readable explanation.
        "summary": summary,

        "reason": reason,

        "explanation": [
            reason
        ],

        # Images do not use news evidence sources.
        "sources": [],

        "source_details": []

    }