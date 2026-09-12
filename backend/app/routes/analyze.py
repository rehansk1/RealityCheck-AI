from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

import os
import shutil
import requests

from bs4 import BeautifulSoup

from app.models import TextRequest

from app.services.gemini_service import (
    verify_news,
    verify_url
)

from app.file_reader import extract_text


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["News Analysis"]
)


# ============================================================
# URL REQUEST MODEL
# ============================================================

class URLRequest(BaseModel):

    url: str


# ============================================================
# EXTRACT ARTICLE TEXT FROM URL
# ============================================================

def extract_article_from_url(url: str):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=25
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unable to access article URL: {str(e)}"
            )
        )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove unwanted elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
        "noscript",
        "iframe"
    ]):

        element.decompose()

    # Try article element first
    article = soup.find("article")

    if article:

        text = article.get_text(
            separator=" ",
            strip=True
        )

    else:

        paragraphs = soup.find_all("p")

        text = " ".join(
            paragraph.get_text(
                separator=" ",
                strip=True
            )
            for paragraph in paragraphs
        )

    text = " ".join(
        text.split()
    )

    return text


# ============================================================
# VERIFY NEWS TEXT
# ============================================================

@router.post("/verify-news")
async def verify_news_text(
    request: TextRequest
):

    try:

        text = request.text.strip()

        if not text:

            raise HTTPException(
                status_code=400,
                detail="Please provide news text."
            )

        print(
            "Received news for verification..."
        )

        result = await verify_news(
            text
        )

        return result

    except HTTPException:
        raise

    except Exception as e:

        print(
            "News verification error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"News verification failed: {str(e)}"
            )
        )


# ============================================================
# ANALYZE TEXT
# ============================================================

@router.post("/analyze-text")
async def analyze_text(
    request: TextRequest
):

    try:

        text = request.text.strip()

        if not text:

            raise HTTPException(
                status_code=400,
                detail="Please provide news text."
            )

        print(
            "Received news for analysis..."
        )

        result = await verify_news(
            text
        )

        return result

    except HTTPException:
        raise

    except Exception as e:

        print(
            "Analysis error:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"News analysis failed: {str(e)}"
            )
        )


# ============================================================
# UPLOAD IMAGE / PDF / DOCX / TXT
# ============================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    try:

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # SUPPORTED FILE EXTENSIONS
        # ----------------------------------------------------

        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }

        document_extensions = {
            ".pdf",
            ".docx",
            ".txt"
        }

        allowed_extensions = (
            image_extensions |
            document_extensions
        )

        # ----------------------------------------------------
        # CHECK EXTENSION
        # ----------------------------------------------------

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Supported files are: "
                    "JPG, JPEG, PNG, WEBP, PDF, DOCX and TXT."
                )
            )

        # ----------------------------------------------------
        # UPLOAD FOLDER
        # ----------------------------------------------------

        upload_folder = "uploads"

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_folder,
            filename
        )

        print("")
        print("================================")
        print("FILE UPLOAD")
        print("================================")
        print("Filename:", filename)
        print("Extension:", extension)

        # ----------------------------------------------------
        # SAVE FILE
        # ----------------------------------------------------

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

        # ====================================================
        # IMAGE
        # ====================================================

        if extension in image_extensions:

            print(
                "Image file detected."
            )

            try:

                from PIL import Image

                from app.detector import detect_ai

                # Open image
                image = Image.open(
                    file_path
                )

                # Convert to RGB
                if image.mode != "RGB":

                    image = image.convert(
                        "RGB"
                    )

                print(
                    "Running AI image detector..."
                )

                result = detect_ai(
                    image
                )

                # Add file information
                result["filename"] = filename
                result["file_type"] = "image"

                print(
                    "IMAGE RESULT:"
                )

                print(
                    result
                )

                return result

            except Exception as e:

                print(
                    "IMAGE ANALYSIS ERROR:",
                    type(e).__name__,
                    str(e)
                )

                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"Image analysis failed: {str(e)}"
                    )
                )

        # ====================================================
        # PDF / DOCX / TXT
        # ====================================================

        if extension in document_extensions:

            print(
                "Document file detected."
            )

            try:

                text = extract_text(
                    file_path,
                    extension
                )

            except Exception as e:

                print(
                    "TEXT EXTRACTION ERROR:",
                    type(e).__name__,
                    str(e)
                )

                raise HTTPException(
                    status_code=500,
                    detail=(
                        "Could not read this document: "
                        f"{str(e)}"
                    )
                )

            if not text or not text.strip():

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Could not extract text from "
                        "this file."
                    )
                )

            print(
                "Extracted characters:",
                len(text)
            )

            # Limit text
            text = text[:18000]

            print(
                "Sending document to news verification..."
            )

            result = await verify_news(
                text
            )

            result["filename"] = filename
            result["file_type"] = "document"

            return result

        # ----------------------------------------------------
        # SAFETY FALLBACK
        # ----------------------------------------------------

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type."
            )
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
            detail=(
                f"File analysis failed: {str(e)}"
            )
        )


# ============================================================
# ANALYZE ARTICLE URL
# ============================================================

@router.post("/analyze-url")
async def analyze_url(
    request: URLRequest
):

    try:

        url = request.url.strip()

        if not url:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Please provide an article URL."
                )
            )

        if not (
            url.startswith("http://")
            or url.startswith("https://")
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Please enter a valid URL."
                )
            )

        print("")
        print("================================")
        print("ARTICLE URL")
        print("================================")
        print(url)

        # ----------------------------------------------------
        # EXTRACT ARTICLE
        # ----------------------------------------------------

        article_text = extract_article_from_url(
            url
        )

        if not article_text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract article text "
                    "from this URL."
                )
            )

        print(
            "Article characters:",
            len(article_text)
        )

        # ----------------------------------------------------
        # LIMIT ARTICLE
        # ----------------------------------------------------

        article_text = article_text[:18000]

        # ----------------------------------------------------
        # VERIFY URL
        # ----------------------------------------------------

        result = await verify_url(
            url,
            article_text
        )

        # Add URL
        result["url"] = url

        return result

    except HTTPException:
        raise

    except Exception as e:

        print(
            "URL ANALYSIS ERROR:",
            type(e).__name__,
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"URL analysis failed: {str(e)}"
            )
        )