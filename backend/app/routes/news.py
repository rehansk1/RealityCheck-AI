from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.models import TextRequest
from app.services.gemini_service import verify_news
from app.file_reader import extract_text


router = APIRouter(
    tags=["News Analysis"]
)


# =====================================================
# FORMAT GEMINI RESULT
# =====================================================

def format_result(result, filename=None):

    return {
        "success": True,

        "filename": filename,

        "prediction": result.get(
            "verdict",
            "UNCERTAIN"
        ),

        "confidence": result.get(
            "confidence",
            0
        ),

        "summary": result.get(
            "summary",
            "Insufficient evidence was found."
        ),

        "explanation": [
            result.get(
                "reason",
                "No explanation was provided."
            )
        ],

        "sources": result.get(
            "sources",
            []
        ),

        # Extra fields for frontend
        "verdict": result.get(
            "verdict",
            "UNCERTAIN"
        ),

        "reason": result.get(
            "reason",
            "Insufficient evidence was found."
        ),

        "claim": result.get(
            "claim",
            ""
        ),

        "evidence_summary": result.get(
            "evidence_summary",
            result.get(
                "summary",
                ""
            )
        ),

        "source_quality": result.get(
            "source_quality",
            "Unknown"
        ),

        "articles": result.get(
            "articles",
            []
        ),

        "total_results": len(
            result.get(
                "articles",
                []
            )
        )
    }


# =====================================================
# VERIFY NEWS TEXT
# =====================================================

@router.post("/verify-news")
async def verify_news_text(
    request: TextRequest
):

    try:

        if not request.text or not request.text.strip():

            raise HTTPException(
                status_code=400,
                detail="Please provide news text."
            )

        print("Received news for verification...")

        # IMPORTANT:
        # verify_news() is synchronous.
        # DO NOT use await here.
        result = verify_news(
            request.text.strip()
        )

        print("Verification completed.")

        return format_result(result)

    except HTTPException:
        raise

    except Exception as e:

        print(
            "News verification error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"News verification failed: {str(e)}"
        )


# =====================================================
# ANALYZE NEWS TEXT
# =====================================================

@router.post("/analyze-text")
async def analyze_text(
    request: TextRequest
):

    try:

        if not request.text or not request.text.strip():

            raise HTTPException(
                status_code=400,
                detail="Please provide news text."
            )

        print("Received news for analysis...")

        result = verify_news(
            request.text.strip()
        )

        print("Analysis completed.")

        return format_result(result)

    except HTTPException:
        raise

    except Exception as e:

        print(
            "Analysis error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"News analysis failed: {str(e)}"
        )


# =====================================================
# FILE UPLOAD
# =====================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    try:

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No file selected."
            )

        filename = os.path.basename(
            file.filename
        )

        extension = os.path.splitext(
            filename
        )[1].lower()

        allowed = [
            ".pdf",
            ".docx",
            ".txt"
        ]

        if extension not in allowed:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only PDF, DOCX and TXT files "
                    "are supported."
                )
            )

        # =================================================
        # UPLOAD FOLDER
        # =================================================

        upload_folder = "uploads"

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_folder,
            filename
        )

        print(
            "Uploading file:",
            filename
        )

        # =================================================
        # SAVE FILE
        # =================================================

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(
            "File saved:",
            file_path
        )

        # =================================================
        # EXTRACT TEXT
        # =================================================

        print(
            "Extracting text..."
        )

        text = extract_text(
            file_path,
            extension
        )

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text from this file. "
                    "Make sure the PDF/DOCX/TXT contains "
                    "readable text."
                )
            )

        print(
            "Extracted characters:",
            len(text)
        )

        # =================================================
        # VERIFY EXTRACTED TEXT
        # =================================================

        print(
            "Sending extracted text to Gemini..."
        )

        result = verify_news(
            text.strip()
        )

        print(
            "File analysis completed."
        )

        return format_result(
            result,
            filename
        )

    except HTTPException:
        raise

    except Exception as e:

        print(
            "FILE UPLOAD ERROR:",
            type(e).__name__,
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"File analysis failed: {str(e)}"
        )