"""Subtitler - Simple and elegant Python library for extracting video subtitles and transcripts."""

__version__ = "0.1.0"

from .constants import DEFAULT_LANGUAGES
from .core.subtitle_extractor import extract_subtitles
from ._exceptions import (
    InvalidVideoInputError,
    SubtitleExtractionError,
    SubtitlerError,
    VideoIdExtractionError,
)


__all__ = [
    "extract_subtitles",
    "SubtitlerError",
    "InvalidVideoInputError",
    "VideoIdExtractionError",
    "SubtitleExtractionError",
    "DEFAULT_LANGUAGES",
]
