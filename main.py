"""FastAPI web service for YouTube subtitle extraction."""

import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

from subtitler.core.subtitle_extractor import extract_subtitles
from subtitler._exceptions import (
    InvalidVideoInputError,
    SubtitleExtractionError,
)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="YouTube Subtitle Extractor API",
    description="Extract subtitles from YouTube videos",
    version="1.0.0"
)

# Security
security = HTTPBearer()

# API Key from environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")


class SubtitleRequest(BaseModel):
    """Request model for subtitle extraction."""
    video_url: str
    languages: Optional[list[str]] = None


class SubtitleResponse(BaseModel):
    """Response model for subtitle extraction."""
    subtitles: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: str


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the API key from the Authorization header."""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.post(
    "/extract-subtitles",
    response_model=SubtitleResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid video input"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        500: {"model": ErrorResponse, "description": "Subtitle extraction failed"},
    }
)
async def extract_subtitles_endpoint(
    request: SubtitleRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Extract subtitles from a YouTube video.

    Args:
        request: The subtitle extraction request containing video_url and optional languages
        api_key: The API key for authentication (provided via Authorization header)

    Returns:
        SubtitleResponse: The extracted subtitles

    Raises:
        HTTPException: For various error conditions (invalid input, extraction failure, etc.)
    """
    try:
        subtitles = extract_subtitles(
            video_url=request.video_url,
            languages=request.languages
        )
        return SubtitleResponse(subtitles=subtitles)

    except InvalidVideoInputError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

    except SubtitleExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        ) from e


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
