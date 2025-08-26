"""Core subtitle extraction functionality."""

from typing import Optional

from youtube_transcript_api import (
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

from ..constants import DEFAULT_LANGUAGES
from ..exceptions import InvalidVideoInputError, SubtitleExtractionError
from ..utils import extract_video_id, validate_video_id, validate_youtube_url


class SubtitleExtractor:
    """Main class for extracting YouTube video subtitles and transcripts."""

    def __init__(self, default_languages: Optional[list[str]] = None):
        """
        Initialize the subtitle extractor.

        Args:
            default_languages: List of preferred languages for subtitles/transcripts
        """
        self.default_languages = default_languages or DEFAULT_LANGUAGES
        self._api = YouTubeTranscriptApi()

    def extract_subtitles(
        self, video_input: str, languages: Optional[list[str]] = None
    ) -> str:
        """
        Extract the subtitles/transcript for a YouTube video by its ID or URL.

        Args:
            video_input: The YouTube video ID or URL
            languages: List of preferred languages (defaults to instance default)

        Returns:
            The complete subtitles/transcript as a single string

        Raises:
            InvalidVideoInputError: If video_input is invalid
            SubtitleExtractionError: If subtitle extraction fails
        """
        if not isinstance(video_input, str) or not video_input.strip():
            raise InvalidVideoInputError("Video input must be a non-empty string")

        video_id = self._extract_video_id_from_input(video_input.strip())
        languages = languages or self.default_languages

        try:
            fetched_transcript = self._api.fetch(video_id, languages=languages)
            return " ".join([snippet.text for snippet in fetched_transcript])

        except TranscriptsDisabled as e:
            raise SubtitleExtractionError(
                f"Subtitles are disabled for video {video_id}"
            ) from e
        except VideoUnavailable as e:
            raise SubtitleExtractionError(f"Video {video_id} is unavailable") from e
        except Exception as e:
            raise SubtitleExtractionError(
                f"Failed to extract subtitles for {video_id}: {str(e)}"
            ) from e

    def _extract_video_id_from_input(self, video_input: str) -> str:
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
