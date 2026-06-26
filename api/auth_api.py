from flask import Blueprint, jsonify

auth_api = Blueprint(
    "auth_api",
    __name__
)


@auth_api.route("/api/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "healthy",
        "service": "trek-booking-api"
    })
