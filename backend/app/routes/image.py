from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io

from app.detector import detect_ai


router = APIRouter(
    prefix="/api",
    tags=["Image Detection"]
)


@router.post("/detect-image")
async def detect_image(
    file: UploadFile = File(...)
):

    try:

        # =====================================================
        # CHECK FILE
        # =====================================================

        if not file or not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Please upload an image."
            )


        # =====================================================
        # CHECK EXTENSION
        # =====================================================

        filename = file.filename.lower()

        allowed_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        )

        if not filename.endswith(
            allowed_extensions
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, JPEG, PNG and WEBP "
                    "images are supported."
                )
            )


        # =====================================================
        # READ FILE
        # =====================================================

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded image is empty."
            )


        # =====================================================
        # OPEN IMAGE
        # =====================================================

        try:

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            image.load()

        except Exception:

            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid image."
            )


        # =====================================================
        # CONVERT TO RGB
        # =====================================================

        if image.mode != "RGB":

            image = image.convert("RGB")


        # =====================================================
        # AI DETECTION
        # =====================================================

        result = detect_ai(image)


        # =====================================================
        # GET SCORE
        # =====================================================

        score = float(
            result.get(
                "confidence",
                0
            )
        )


        # =====================================================
        # YOUR CLASSIFICATION RULE
        #
        # ABOVE 50%  = REAL
        # 50% OR LESS = FAKE
        # =====================================================

        if score > 50:

            verdict = "REAL"

        else:

            verdict = "FAKE"


        # =====================================================
        # SUMMARY
        # =====================================================

        summary = (
            f"The image received an analysis score of "
            f"{score:.2f}%. Because the score is "
            f"{'above' if score > 50 else '50% or below'} "
            f"the 50.0% threshold, the image is "
            f"classified as {verdict}."
        )


        # =====================================================
        # WHY
        # =====================================================

        reason = (
            f"The analysis score of {score:.2f}% "
            f"is {'greater than' if score > 50 else '50% or less than or equal to'} "
            f"the 50.0% threshold."
        )


        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {

            "success": True,

            "filename": file.filename,

            "verdict": verdict,

            "prediction": verdict,

            "confidence": round(
                score,
                2
            ),

            "summary": summary,

            "reason": reason,

            "explanation": [
                reason
            ],

            "sources": [],

            "source_details": [],

            "relevance": [],

            "message": "Image analyzed successfully"

        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            "IMAGE API ERROR:",
            type(error).__name__,
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Image analysis failed: {str(error)}"
            )
        )