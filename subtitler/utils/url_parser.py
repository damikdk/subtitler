"""URL parsing utilities for YouTube URLs."""

from urllib.parse import parse_qs, urlparse

from ..constants import VALID_YOUTUBE_DOMAINS, YOUTUBE_VIDEO_ID_LENGTH
from ..exceptions import InvalidVideoInputError, VideoIdExtractionError


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
