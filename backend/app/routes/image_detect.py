from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io

from app.detector import detect_ai


router = APIRouter(
    prefix="/api",
    tags=["Image Detection"]
)


@router.post("/detect-image")
async def detect_image(file: UploadFile = File(...)):

    image_bytes = await file.read()

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    result = detect_ai(image)

    return {
        "filename": file.filename,
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "message": "Image analyzed successfully"
    }