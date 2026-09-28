"""
app/utils/response.py
──────────────────────
Standardised JSON response helpers.
Every API response follows the same shape:
  { success, data, message, error }
"""

from flask import jsonify


def success_response(data: dict, message: str = "OK", status_code: int = 200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data,
        "error": None,
    }), status_code


def error_response(message: str, status_code: int = 400, error_code: str = None):
    return jsonify({
        "success": False,
        "message": message,
        "data": None,
        "error": error_code or message,
    }), status_code
