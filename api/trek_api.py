from flask import Blueprint, jsonify

from models.trek import Trek
from api.decorators import token_required

trek_api = Blueprint(
    "trek_api",
    __name__
)


@trek_api.route("/api/treks", methods=["GET"])
@token_required
def get_all_treks():

    treks = Trek.query.all()

    response = []

    for trek in treks:

        response.append({
            "id": trek.id,
            "name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "available_slots": trek.available_slots,
            "status": trek.status
        })

    return jsonify(response), 200
