from functools import wraps
from flask import request, jsonify

API_TOKEN = "TREK_APP_SECRET_2026"


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({
                "success": False,
                "message": "Token missing"
            }), 401

        if token != API_TOKEN:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 403

        return f(*args, **kwargs)

    return decorated
