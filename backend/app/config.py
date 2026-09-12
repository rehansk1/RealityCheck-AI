from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Upload folder
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)


# AI Models
FAKE_NEWS_MODEL = os.getenv(
    "FAKE_NEWS_MODEL",
    "hamzab/roberta-fake-news-classification"
)


SUMMARIZER_MODEL = os.getenv(
    "SUMMARIZER_MODEL",
    "google/flan-t5-small"
)


# API Settings
APP_NAME = "RealityCheck AI"
APP_VERSION = "1.0.0"


# File Upload Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}