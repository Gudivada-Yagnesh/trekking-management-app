from datetime import date

from models import db
from models.booking import Booking
from models.trek import Trek

from services.concurrency_manager import booking_lock


class SafeBookingProcessor:

    @staticmethod
    def process_booking(user_id, trek_id):

        """
        Thread-safe booking processor.

        Prevents:
        - Race conditions
        - Duplicate bookings
        - Overbooking
        """

        with booking_lock:

            trek = Trek.query.get(trek_id)

            if not trek:
                return {
                    "success": False,
                    "message": "Trek not found"
                }

            if trek.status.lower() != "open":
                return {
                    "success": False,
                    "message": "Trek is not open for booking"
                }

            if trek.available_slots <= 0:
                return {
                    "success": False,
                    "message": "No slots available"
                }

            existing_booking = Booking.query.filter_by(
                user_id=user_id,
                trek_id=trek_id
            ).first()

            if existing_booking:
                return {
                    "success": False,
                    "message": "Duplicate booking not allowed"
                }

            try:

                booking = Booking(
                    user_id=user_id,
                    trek_id=trek_id,
                    booking_date=date.today(),
                    status="BOOKED",
                    payment_status="PENDING"
                )

                db.session.add(booking)

                # Critical section
                trek.available_slots -= 1

                db.session.commit()

                return {
                    "success": True,
                    "message": "Booking successful"
                }

            except Exception as e:

                db.session.rollback()

                return {
                    "success": False,
                    "message": str(e)
                }
