"""
app/utils/validators.py
────────────────────────
Input validation helpers.
"""

from urllib.parse import urlparse
from config import Config


def is_valid_instagram_url(url: str) -> bool:
    """
    Returns True only if the URL is a valid Instagram link.
    Supported patterns:
      - /reel/
      - /p/        (post)
      - /stories/
      - /tv/
    """
    if not url or not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url.strip())
    except Exception:
        return False

    # Must be http or https
    if parsed.scheme not in ("http", "https"):
        return False

    # Must be instagram domain
    if parsed.netloc not in Config.SUPPORTED_DOMAINS:
        return False

    # Must contain a recognisable path segment
    valid_paths = ("/reel/", "/p/", "/stories/", "/tv/")
    if not any(segment in parsed.path for segment in valid_paths):
        return False

    return True


def sanitize_url(url: str) -> str:
    """Strip trailing slashes and whitespace."""
    return url.strip().rstrip("/")
