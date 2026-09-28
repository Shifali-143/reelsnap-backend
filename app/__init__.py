"""
app/__init__.py
────────────────
Flask application factory.
Creates and configures the Flask app instance.
"""

from flask import Flask
from flask_cors import CORS

from config import Config
from app.routes import download_bp, health_bp


def create_app() -> Flask:
    """
    Application factory pattern.
    Returns a fully configured Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # ── CORS ──────────────────────────────────────
    CORS(app, origins=Config.ALLOWED_ORIGINS)

    # ── Register Blueprints ───────────────────────
    app.register_blueprint(health_bp)
    app.register_blueprint(download_bp)

    # ── Global error handlers ─────────────────────
    @app.errorhandler(404)
    def not_found(e):
        from app.utils import error_response
        return error_response("Route not found.", 404, "NOT_FOUND")

    @app.errorhandler(405)
    def method_not_allowed(e):
        from app.utils import error_response
        return error_response("Method not allowed.", 405, "METHOD_NOT_ALLOWED")

    @app.errorhandler(500)
    def internal_error(e):
        from app.utils import error_response
        return error_response("Internal server error.", 500, "INTERNAL_ERROR")

    return app
