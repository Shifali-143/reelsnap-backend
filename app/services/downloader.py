"""
app/services/downloader.py
───────────────────────────
Core download service using yt-dlp.
This is the ONLY place in the entire codebase that touches yt-dlp.
All routes call this service — never yt-dlp directly.

Instagram requires cookies for most content since 2023.
Two supported methods (set in .env):
  1. INSTAGRAM_COOKIE_FILE  → path to a cookies.txt (Netscape format)
  2. INSTAGRAM_COOKIE_BROWSER → browser name e.g. "chrome", "safari", "firefox"
     (yt-dlp reads cookies from that browser automatically)
"""

import os
import yt_dlp
from config import Config


class DownloadService:
    """Handles all media extraction logic via yt-dlp."""

    # ── Public methods ─────────────────────────────────────────────────────

    def get_video_info(self, url: str) -> dict:
        """
        Extract video/reel metadata + direct download URL.
        Returns a dict with all available formats.
        """
        opts = {
            **Config.YTDLP_OPTIONS,
            "format": "bestvideo+bestaudio/best",
        }
        return self._extract(url, opts)

    def get_audio_info(self, url: str) -> dict:
        """
        Extract audio-only stream URL.
        For Instagram, this gives the background audio/song.
        """
        opts = {
            **Config.YTDLP_OPTIONS,
            "format": "bestaudio/best",
        }
        return self._extract(url, opts)

    def get_story_info(self, url: str) -> dict:
        """
        Extract Instagram story/status URL.
        Stories follow the same extraction path as reels.
        """
        return self.get_video_info(url)

    # ── Private helpers ────────────────────────────────────────────────────

    def _build_cookie_opts(self) -> dict:
        """
        Return cookie options for yt-dlp based on .env config.
        Priority: cookie file > browser > none
        """
        cookie_file    = os.getenv("INSTAGRAM_COOKIE_FILE", "").strip()
        cookie_browser = os.getenv("INSTAGRAM_COOKIE_BROWSER", "").strip()

        if cookie_file and os.path.exists(cookie_file):
            return {"cookiefile": cookie_file}

        if cookie_browser:
            return {"cookiesfrombrowser": (cookie_browser,)}

        return {}  # No cookies — works only for truly public content

    def _extract(self, url: str, opts: dict) -> dict:
        """
        Core extraction — calls yt-dlp and returns normalised data.
        Raises ValueError on failure so routes can catch cleanly.
        """
        # Merge cookie opts — they override nothing else
        full_opts = {**opts, **self._build_cookie_opts()}

        try:
            with yt_dlp.YoutubeDL(full_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            return self._normalise(info)

        except yt_dlp.utils.DownloadError as e:
            raw = str(e)
            # Give user-friendly messages for common Instagram errors
            if "login required" in raw.lower() or "rate-limit" in raw.lower():
                raise ValueError(
                    "Instagram requires authentication to access this content. "
                    "Configure INSTAGRAM_COOKIE_BROWSER in your .env file."
                )
            raise ValueError(f"Could not fetch media: {raw}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    def _normalise(self, info: dict) -> dict:
        """
        Convert raw yt-dlp info dict into a clean, frontend-friendly shape.
        Only expose what the frontend actually needs.
        Deduplicates by (quality + type) so same resolution never shows twice.
        """
        formats = info.get("formats", [])

        # Build a clean list of available formats
        available = []
        seen_qualities = set()   # dedupe by "720p-video", "128kbps-audio" etc.

        for fmt in formats:
            url = fmt.get("url")
            if not url:
                continue

            ext = fmt.get("ext", "mp4")
            height = fmt.get("height")
            abr = fmt.get("abr")  # audio bitrate

            # Label quality and type
            if height:
                quality    = f"{height}p"
                media_type = "video"
            elif abr:
                quality    = f"{int(abr)}kbps"
                media_type = "audio"
            else:
                quality    = "default"
                media_type = "video"

            # Skip duplicate quality+type combos
            dedup_key = f"{quality}-{media_type}"
            if dedup_key in seen_qualities:
                continue
            seen_qualities.add(dedup_key)

            available.append({
                "url": url,
                "quality": quality,
                "ext": ext,
                "type": media_type,
            })

        # Sort video formats nicely: highest quality first
        def _quality_num(f: dict) -> int:
            """Parse numeric part of quality string safely (e.g. '720p' → 720, '128kbps' → 128, '78kbs' → 78)."""
            raw = f["quality"]
            cleaned = raw.replace("kbps", "").replace("kbs", "").replace("p", "").strip()
            try:
                return int(cleaned)
            except ValueError:
                return 0

        available.sort(key=lambda f: (
            0 if f["type"] == "video" else 1,   # video first, audio last
            -_quality_num(f),                    # highest quality first within each type
        ))

        # Best single URL (fallback)
        best_url = info.get("url") or (available[0]["url"] if available else None)

        return {
            "title": info.get("title", "Instagram Media"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "best_url": best_url,
            "formats": available,
        }


# Singleton — import this instance everywhere
download_service = DownloadService()