"""
app/routes/health.py
─────────────────────
Health check endpoint.
Used by Render.com, UptimeRobot, and load balancers
to confirm the server is alive.
"""

from flask import Blueprint
from app.utils import success_response

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    """GET /api/health → { success: true, data: { status: "ok" } }"""
    return success_response({"status": "ok"}, "Server is running.")
