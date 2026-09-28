"""
app/middlewares/rate_limiter.py
────────────────────────────────
Simple in-memory rate limiter (per IP, per minute).
For production at scale → swap this with Redis-based limiter.
"""

import time
from collections import defaultdict
from functools import wraps

from flask import request
from config import Config
from app.utils import error_response


# { ip_address: [timestamp, timestamp, ...] }
_request_log: dict[str, list[float]] = defaultdict(list)


def rate_limit(f):
    """
    Decorator — limits each IP to Config.RATE_LIMIT requests per minute.
    Apply to any route that should be protected.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = _get_client_ip()
        now = time.time()
        window = 60  # seconds

        # Remove timestamps older than 1 minute
        _request_log[ip] = [
            ts for ts in _request_log[ip] if now - ts < window
        ]

        if len(_request_log[ip]) >= Config.RATE_LIMIT:
            return error_response(
                message=f"Too many requests. Max {Config.RATE_LIMIT} per minute.",
                status_code=429,
                error_code="RATE_LIMIT_EXCEEDED",
            )

        _request_log[ip].append(now)
        return f(*args, **kwargs)

    return decorated


def _get_client_ip() -> str:
    """Get real client IP, handles proxies (Render, Cloudflare, etc.)."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"
