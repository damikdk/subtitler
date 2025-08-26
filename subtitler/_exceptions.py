"""Custom exceptions for the Subtitler package (kept separate to avoid cycles)."""


class SubtitlerError(Exception):
    """Base exception for subtitle extraction errors."""

    pass


class InvalidVideoInputError(SubtitlerError):
    """Raised when the video input (URL or ID) is invalid."""

    pass


class VideoIdExtractionError(SubtitlerError):
    """Raised when video ID cannot be extracted from a URL."""

    pass


class SubtitleExtractionError(SubtitlerError):
    """Raised when subtitle extraction fails for any reason."""

    pass
