"""
config/settings.py
──────────────────
All app configuration loaded from environment variables.
Never hardcode secrets here — use .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Flask ──────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    ENV: str = os.getenv("FLASK_ENV", "production")

    # ── Server ─────────────────────────────────────
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))

    # ── CORS ───────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    ]

    # ── Rate Limiting ──────────────────────────────
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", 10))  # per minute per IP

    # ── yt-dlp options ────────────────────────────
    YTDLP_OPTIONS: dict = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "socket_timeout": 30,
    }

    # ── Supported platforms ───────────────────────
    SUPPORTED_DOMAINS: list[str] = [
        "instagram.com",
        "www.instagram.com",
    ]
