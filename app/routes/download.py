"""
app/routes/download.py
───────────────────────
All /api/download/* endpoints.

Routes:
  POST /api/download/reel    → download reel/video
  POST /api/download/audio   → extract audio only
  POST /api/download/story   → download story/status
"""

from flask import Blueprint, request

from app.services import download_service
from app.utils import (
    is_valid_instagram_url,
    sanitize_url,
    success_response,
    error_response,
)
from app.middlewares import rate_limit

download_bp = Blueprint("download", __name__, url_prefix="/api/download")


# ── Shared helper ──────────────────────────────────────────────────────────

def _get_url_from_request() -> str | None:
    """Extract and validate URL from JSON body."""
    body = request.get_json(silent=True)
    if not body:
        return None
    return body.get("url", "").strip()


# ── Routes ─────────────────────────────────────────────────────────────────

@download_bp.route("/reel", methods=["POST"])
@rate_limit
def download_reel():
    """
    Download an Instagram Reel or video post.

    Request body:
      { "url": "https://www.instagram.com/reel/..." }

    Response:
      { success, data: { title, thumbnail, best_url, formats } }
    """
    url = _get_url_from_request()

    if not url:
        return error_response("URL is required.", 400, "MISSING_URL")

    if not is_valid_instagram_url(url):
        return error_response("Invalid Instagram URL.", 400, "INVALID_URL")

    url = sanitize_url(url)

    try:
        data = download_service.get_video_info(url)
        return success_response(data, "Reel fetched successfully.")
    except ValueError as e:
        return error_response(str(e), 422, "EXTRACTION_FAILED")


@download_bp.route("/audio", methods=["POST"])
@rate_limit
def download_audio():
    """
    Extract audio from an Instagram Reel.

    Request body:
      { "url": "https://www.instagram.com/reel/..." }

    Response:
      { success, data: { title, best_url, formats (audio only) } }
    """
    url = _get_url_from_request()

    if not url:
        return error_response("URL is required.", 400, "MISSING_URL")

    if not is_valid_instagram_url(url):
        return error_response("Invalid Instagram URL.", 400, "INVALID_URL")

    url = sanitize_url(url)

    try:
        data = download_service.get_audio_info(url)
        return success_response(data, "Audio fetched successfully.")
    except ValueError as e:
        return error_response(str(e), 422, "EXTRACTION_FAILED")


@download_bp.route("/story", methods=["POST"])
@rate_limit
def download_story():
    """
    Download an Instagram Story or Status.

    Request body:
      { "url": "https://www.instagram.com/stories/..." }

    Response:
      { success, data: { title, thumbnail, best_url, formats } }
    """
    url = _get_url_from_request()

    if not url:
        return error_response("URL is required.", 400, "MISSING_URL")

    if not is_valid_instagram_url(url):
        return error_response("Invalid Instagram URL.", 400, "INVALID_URL")

    url = sanitize_url(url)

    try:
        data = download_service.get_story_info(url)
        return success_response(data, "Story fetched successfully.")
    except ValueError as e:
        return error_response(str(e), 422, "EXTRACTION_FAILED")
