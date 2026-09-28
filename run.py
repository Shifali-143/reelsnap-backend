"""
run.py
───────
Development entry point.
Run with: python run.py

For production use gunicorn (see Procfile / render.yaml).
"""

from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
    )
