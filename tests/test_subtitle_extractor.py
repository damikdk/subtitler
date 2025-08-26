"""Tests for the subtitle extraction functions."""

from unittest.mock import Mock, patch

import pytest
from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable

from subtitler import (
    DEFAULT_LANGUAGES,
    InvalidVideoInputError,
    SubtitleExtractionError,
    extract_subtitles,
)
from subtitler.constants import TEST_VIDEO_IDS, TEST_VIDEO_URLS


class TestSubtitleExtractor:
    """Test cases for subtitle extraction functions."""

    @pytest.mark.parametrize("video_id", TEST_VIDEO_IDS)
    def test_extract_subtitles_with_valid_video_ids(self, video_id):
        """Test extracting subtitles with all valid video IDs from constants."""
        try:
            subtitles = extract_subtitles(video_id)

            # Verify transcript is returned as string
            assert isinstance(subtitles, str)

            # Verify transcript is not empty (most videos should have transcripts)
            assert len(subtitles) > 0

            # Check first 100 characters are reasonable (contain text, not just symbols)
            first_100 = subtitles[:100]
            assert len(first_100.strip()) > 0

            # Basic sanity check - should contain some alphabetic characters
            assert any(c.isalpha() for c in first_100)

        except SubtitleExtractionError:
            # Some test videos might not have transcripts available
            # This is acceptable for testing purposes
            pytest.skip(f"Transcript not available for video {video_id}")

    @pytest.mark.parametrize("video_url", TEST_VIDEO_URLS)
    def test_extract_subtitles_with_valid_video_urls(self, video_url):
        """Test extracting subtitles with all valid video URLs from constants."""
        try:
            subtitles = extract_subtitles(video_url)

            # Verify transcript is returned as string
            assert isinstance(subtitles, str)

            # Verify transcript is not empty (most videos should have transcripts)
            assert len(subtitles) > 0

            # Check first 100 characters are reasonable
            first_100 = subtitles[:100]
            assert len(first_100.strip()) > 0

            # Basic sanity check - should contain some alphabetic characters
            assert any(c.isalpha() for c in first_100)

        except SubtitleExtractionError:
            # Some test videos might not have transcripts available
            # This is acceptable for testing purposes
            pytest.skip(f"Transcript not available for URL {video_url}")

    def test_extract_subtitles_with_custom_languages(self):
        """Test extracting subtitles with custom language preferences."""
        # Use first test video ID
        video_id = TEST_VIDEO_IDS[0]
        custom_languages = ["es", "en", "fr"]

        try:
            subtitles = extract_subtitles(video_id, languages=custom_languages)
            assert isinstance(subtitles, str)
            assert len(subtitles) > 0
        except SubtitleExtractionError:
            pytest.skip(f"Transcript not available for video {video_id}")

    def test_extract_subtitles_empty_input(self):
        """Test that empty input raises InvalidVideoInputError."""
        with pytest.raises(
            InvalidVideoInputError, match="Video input must be a non-empty string"
        ):
            extract_subtitles("")

    def test_extract_subtitles_whitespace_only_input(self):
        """Test that whitespace-only input raises InvalidVideoInputError."""
        with pytest.raises(
            InvalidVideoInputError, match="Video input must be a non-empty string"
        ):
            extract_subtitles("   ")

    def test_extract_subtitles_none_input(self):
        """Test that None input raises InvalidVideoInputError."""
        with pytest.raises(
            InvalidVideoInputError, match="Video input must be a non-empty string"
        ):
            extract_subtitles(None)

    def test_extract_subtitles_non_string_input(self):
        """Test that non-string input raises InvalidVideoInputError."""
        with pytest.raises(
            InvalidVideoInputError, match="Video input must be a non-empty string"
        ):
            extract_subtitles(123)

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "https://www.google.com",
            "https://vimeo.com/123456",
            "not_a_url_at_all",
            "https://youtube.com/watch?v=",  # No video ID
            "https://youtube.com/watch?v=invalid",  # Invalid video ID format
            "https://youtube.com/watch?v=123",  # Too short video ID
            "https://youtube.com/watch?v=this_is_too_long_for_video_id",  # Too long video ID
        ],
    )
    def test_extract_subtitles_invalid_urls(self, invalid_url):
        """Test that invalid URLs raise InvalidVideoInputError."""
        with pytest.raises(InvalidVideoInputError, match="Invalid video input"):
            extract_subtitles(invalid_url)

    @pytest.mark.parametrize(
        "invalid_video_id",
        [
            "short",  # Too short
            "this_is_way_too_long_for_a_video_id",  # Too long
            "invalid-chars!",  # Invalid characters
            "invalid@id!",  # Contains invalid characters
        ],
    )
    def test_extract_subtitles_invalid_video_ids(self, invalid_video_id):
        """Test that invalid video IDs raise InvalidVideoInputError."""
        with pytest.raises(InvalidVideoInputError, match="Invalid video input"):
            extract_subtitles(invalid_video_id)

    def test_extract_subtitles_unavailable_video_id(self):
        """Test that a valid format but unavailable video ID raises SubtitleExtractionError."""
        # Use a properly formatted but unavailable video ID
        unavailable_video_id = (
            "123456789AB"  # 11 chars, alphanumeric, but doesn't exist
        )

        with pytest.raises(SubtitleExtractionError, match="Video .* is unavailable"):
            extract_subtitles(unavailable_video_id)

    @patch("subtitler.core.subtitle_extractor.YouTubeTranscriptApi")
    def test_extract_subtitles_transcripts_disabled(self, mock_api_class):
        """Test handling of TranscriptsDisabled exception."""
        mock_api = Mock()
        mock_api.fetch.side_effect = TranscriptsDisabled("video_id")
        mock_api_class.return_value = mock_api

        with pytest.raises(
            SubtitleExtractionError, match="Subtitles are disabled for video"
        ):
            extract_subtitles("dQw4w9WgXcQ")

    @patch("subtitler.core.subtitle_extractor.YouTubeTranscriptApi")
    def test_extract_subtitles_video_unavailable(self, mock_api_class):
        """Test handling of VideoUnavailable exception."""
        mock_api = Mock()
        mock_api.fetch.side_effect = VideoUnavailable("video_id")
        mock_api_class.return_value = mock_api

        with pytest.raises(SubtitleExtractionError, match="Video .* is unavailable"):
            extract_subtitles("dQw4w9WgXcQ")

    @patch("subtitler.core.subtitle_extractor.YouTubeTranscriptApi")
    def test_extract_subtitles_generic_exception(self, mock_api_class):
        """Test handling of generic exceptions."""
        mock_api = Mock()
        mock_api.fetch.side_effect = Exception("Generic error")
        mock_api_class.return_value = mock_api

        with pytest.raises(
            SubtitleExtractionError, match="Failed to extract subtitles"
        ):
            extract_subtitles("dQw4w9WgXcQ")

    @patch("subtitler.core.subtitle_extractor.YouTubeTranscriptApi")
    def test_extract_subtitles_success_mock(self, mock_api_class):
        """Test successful subtitle extraction with mocked response."""
        # Mock transcript data
        mock_transcript = [
            Mock(text="Hello world"),
            Mock(text="This is a test"),
            Mock(text="YouTube transcript"),
        ]

        mock_api = Mock()
        mock_api.fetch.return_value = mock_transcript
        mock_api_class.return_value = mock_api

        result = extract_subtitles("dQw4w9WgXcQ")

        assert result == "Hello world This is a test YouTube transcript"
        mock_api.fetch.assert_called_once_with(
            "dQw4w9WgXcQ", languages=DEFAULT_LANGUAGES
        )

    def test_extract_video_id_from_input_valid_id(self):
        """Test extracting video ID from valid video ID input."""
        from subtitler.core.subtitle_extractor import _extract_video_id_from_input
        video_id = "dQw4w9WgXcQ"
        result = _extract_video_id_from_input(video_id)
        assert result == video_id

    def test_extract_video_id_from_input_valid_url(self):
        """Test extracting video ID from valid URL input."""
        from subtitler.core.subtitle_extractor import _extract_video_id_from_input
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = _extract_video_id_from_input(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_video_id_from_input_invalid(self):
        """Test that invalid input raises InvalidVideoInputError."""
        from subtitler.core.subtitle_extractor import _extract_video_id_from_input
        with pytest.raises(InvalidVideoInputError, match="Invalid video input"):
            _extract_video_id_from_input("invalid_input")


class TestSubtitleExtractorIntegration:
    """Integration tests that require actual network calls."""

    def test_real_video_transcript_fetch(self):
        """Test fetching a real video transcript (marked as slow test)."""
        # Using a well-known video that should have transcripts
        video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up

        try:
            subtitles = extract_subtitles(video_id)

            # Basic validation
            assert isinstance(subtitles, str)
            assert len(subtitles) > 100  # Should be substantial content

            # Check first 100 characters
            first_100 = subtitles[:100]
            assert len(first_100.strip()) > 0
            assert any(c.isalpha() for c in first_100)

        except SubtitleExtractionError as e:
            # If the video doesn't have transcripts, that's still a valid test result
            pytest.skip(f"Video transcript not available: {e}")
