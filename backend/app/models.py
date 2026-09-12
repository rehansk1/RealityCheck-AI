from pydantic import BaseModel, HttpUrl
from typing import List


class TextRequest(BaseModel):
    text: str


class URLRequest(BaseModel):
    url: HttpUrl


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    summary: str
    explanation: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    message: str