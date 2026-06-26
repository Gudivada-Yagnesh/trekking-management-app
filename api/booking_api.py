from flask import Blueprint, jsonify

from models.booking import Booking
from api.decorators import token_required

booking_api = Blueprint(
    "booking_api",
    __name__
)


@booking_api.route("/api/bookings", methods=["GET"])
@token_required
def get_all_bookings():

    bookings = Booking.query.all()

    response = []

    for booking in bookings:

        response.append({
            "booking_id": booking.id,
            "user_id": booking.user_id,
            "trek_id": booking.trek_id,
            "status": booking.status
        })

    return jsonify(response), 200
