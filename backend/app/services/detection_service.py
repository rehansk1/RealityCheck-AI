from app.detector import detect_ai


def analyze_image(image):
    """
    Analyze an image using the AI image detection model.
    """

    if image is None:
        return {
            "prediction": "UNCERTAIN",
            "confidence": 0,
            "message": "No image provided."
        }

    result = detect_ai(image)

    return result