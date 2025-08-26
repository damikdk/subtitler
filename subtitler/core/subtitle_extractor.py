"""Core subtitle extraction functionality."""

from urllib.parse import parse_qs, urlparse
from typing import Optional

from youtube_transcript_api import (
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

from ..constants import (
    DEFAULT_LANGUAGES,
    VALID_YOUTUBE_DOMAINS,
    YOUTUBE_VIDEO_ID_LENGTH,
)
from .._exceptions import (
    InvalidVideoInputError,
    SubtitleExtractionError,
    VideoIdExtractionError,
)


def extract_subtitles(
    video_input: str, languages: Optional[list[str]] = None
) -> str:
    """
    Extract the subtitles/transcript for a YouTube video by its ID or URL.

    Args:
        video_input: The YouTube video ID or URL
        languages: List of preferred languages (defaults to DEFAULT_LANGUAGES)

    Returns:
        The complete subtitles/transcript as a single string

    Raises:
        InvalidVideoInputError: If video_input is invalid
        SubtitleExtractionError: If subtitle extraction fails
    """
    if not isinstance(video_input, str) or not video_input.strip():
        raise InvalidVideoInputError(
            "Video input must be a non-empty string")

    video_id = _extract_video_id_from_input(video_input.strip())
    languages = languages or DEFAULT_LANGUAGES

    try:
        api = YouTubeTranscriptApi()
        fetched_transcript = api.fetch(video_id, languages=languages)
        return " ".join([snippet.text for snippet in fetched_transcript])

    except TranscriptsDisabled as e:
        raise SubtitleExtractionError(
            f"Subtitles are disabled for video {video_id}"
        ) from e
    except VideoUnavailable as e:
        raise SubtitleExtractionError(
            f"Video {video_id} is unavailable") from e
    except Exception as e:
        raise SubtitleExtractionError(
            f"Failed to extract subtitles for {video_id}: {str(e)}"
        ) from e


def _extract_video_id_from_input(video_input: str) -> str:
    """
    Extract video ID from either a URL or validate a direct video ID.

    Args:
        video_input: YouTube URL or video ID

    Returns:
        Valid video ID

    Raises:
        InvalidVideoInputError: If input is invalid
    """
    # Check if it's a URL
    if validate_youtube_url(video_input):
        return extract_video_id(video_input)

    # Check if it's a direct video ID
    if validate_video_id(video_input):
        return video_input

    raise InvalidVideoInputError(
        f"Invalid video input: {video_input}. Must be a valid YouTube URL or 11-character video ID"
    )


# ---- Inlined helpers (moved from subtitler/utils/url_parser.py) ----


def validate_youtube_url(url: str) -> bool:
    """
    Validate that the provided URL is a valid YouTube video URL.

    Args:
        url: The URL string to validate

    Returns:
        True if the URL is a valid YouTube video URL, False otherwise
    """
    if not isinstance(url, str) or not url.strip():
        return False

    try:
        parsed = urlparse(url.strip())

        # Check for valid YouTube domains
        if parsed.netloc.lower() not in VALID_YOUTUBE_DOMAINS:
            return False

        # For youtu.be format
        if parsed.netloc.lower() == "youtu.be":
            # Path should contain video ID (11 characters)
            video_id = parsed.path.lstrip("/")
            return len(video_id) == YOUTUBE_VIDEO_ID_LENGTH and video_id.isalnum()

        # For youtube.com format
        if parsed.path in ["/watch", "/watch/"]:
            query_params = parse_qs(parsed.query)
            if "v" in query_params and query_params["v"]:
                video_id = query_params["v"][0]
                return (
                    len(video_id) == YOUTUBE_VIDEO_ID_LENGTH
                    and video_id.replace("_", "").replace("-", "").isalnum()
                )

        return False

    except Exception:
        return False


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from a YouTube URL.

    Args:
        url: The YouTube URL string

    Returns:
        The video ID if successfully extracted

    Raises:
        InvalidVideoInputError: If the URL is invalid
        VideoIdExtractionError: If video ID cannot be extracted
    """
    if not validate_youtube_url(url):
        raise InvalidVideoInputError(f"Invalid YouTube URL: {url}")

    try:
        parsed = urlparse(url.strip())

        # For youtu.be format
        if parsed.netloc.lower() == "youtu.be":
            return parsed.path.lstrip("/")

        # For youtube.com format
        if parsed.path in ["/watch", "/watch/"]:
            query_params = parse_qs(parsed.query)
            if "v" in query_params and query_params["v"]:
                return query_params["v"][0]

        raise VideoIdExtractionError(
            f"Could not extract video ID from URL: {url}")

    except (InvalidVideoInputError, VideoIdExtractionError):
        raise
    except Exception as e:
        raise VideoIdExtractionError(
            f"Failed to extract video ID: {str(e)}") from e


def validate_video_id(video_id: str) -> bool:
    """
    Validate that the provided string is a valid YouTube video ID.

    Args:
        video_id: The video ID string to validate

    Returns:
        True if the video ID is valid, False otherwise
    """
    if not isinstance(video_id, str) or not video_id.strip():
        return False

    video_id = video_id.strip()
    return (
        len(video_id) == YOUTUBE_VIDEO_ID_LENGTH
        and video_id.replace("_", "").replace("-", "").isalnum()
    )
