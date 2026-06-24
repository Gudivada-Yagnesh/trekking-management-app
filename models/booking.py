# SQLAlchemy database object ni import chesthunam
from models import db

# Booking table model
class Booking(db.Model):

    # SQLite table name
    __tablename__ = "bookings"

    # Booking unique identifier
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user = db.relationship(
        "User",
        backref="bookings"
    )

    trek = db.relationship(
        "Trek",
        backref="bookings"
    )
    # User reference
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Trek reference
    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    # Booking date
    booking_date = db.Column(
        db.Date,
        nullable=False
    )

    # Booking status
    status = db.Column(
        db.String(30),
        nullable=False
    )

    # Payment status
    payment_status = db.Column(
        db.String(30),
        nullable=False
    )

    # Duplicate bookings prevent cheyyadaniki composite unique constraint
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "trek_id",
            name="unique_user_trek_booking"
        ),
    )
