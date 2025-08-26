"""Subtitler - Simple and elegant Python library for extracting video subtitles and transcripts."""

__version__ = "0.1.0"

from typing import Optional

from .constants import DEFAULT_LANGUAGES
from .core import SubtitleExtractor
from .exceptions import (
    InvalidVideoInputError,
    SubtitleExtractionError,
    SubtitlerError,
    VideoIdExtractionError,
)


def extract_subtitles(video_input: str, languages: Optional[list[str]] = None) -> str:
    """
    Extract subtitles/transcript for a YouTube video.

    Args:
        video_input: YouTube URL or video ID
        languages: Preferred languages (optional)

    Returns:
        Complete subtitles/transcript as string
    """
    extractor = SubtitleExtractor()
    return extractor.extract_subtitles(video_input, languages)


__all__ = [
    "extract_subtitles",
    "SubtitleExtractor",
    "SubtitlerError",
    "InvalidVideoInputError",
    "VideoIdExtractionError",
    "SubtitleExtractionError",
    "DEFAULT_LANGUAGES",
]
