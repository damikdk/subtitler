"""Constants for the Subtitler package."""


# Top 20 languages by number of speakers
DEFAULT_LANGUAGES: list[str] = [
    "en",
    "fr",
    "es",
    "de",
    "ru",
    "zh",
    "it",
    "pt",
    "ja",
    "ar",
    "hi",
    "bn",
    "pa",
    "te",
    "ta",
    "ml",
    "mr",
    "gu",
    "kn",
    "or",
    "nl",
    "pl",
    "ro",
    "sv",
    "tr",
    "uk",
    "vi",
    "yo",
    "zu",
]

# Valid YouTube domains
VALID_YOUTUBE_DOMAINS: set[str] = {
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "m.youtube.com",
}

# YouTube video ID length
YOUTUBE_VIDEO_ID_LENGTH: int = 11

# Test video IDs for development and testing
TEST_VIDEO_IDS: list[str] = [
    "NgsWGfUlwJI",  # TED Talk with captions
    "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
    "fGkCY5z3D_c",  # Educational content
    "0xyxtzD54rM",  # Tech tutorial
    "UD8EkZOKZwA",  # Conference talk
]

# Test video URLs for development and testing
TEST_VIDEO_URLS: list[str] = [
    "https://www.youtube.com/watch?v=PEBS2jbZce4",
    "https://www.youtube.com/watch?v=PEBS2jbZce4&list=RDPEBS2jbZce4&start_radio=1&pp=oAcB0gcJCbIJAYcqIYzv",
    "https://youtu.be/dQw4w9WgXcQ",
]
