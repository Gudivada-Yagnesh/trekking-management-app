# SQLAlchemy database object ni import chesthunam
from models import db


# Treks table ni represent chese model
class Trek(db.Model):

    # SQLite table name
    __tablename__ = "treks"

    # Trek unique identifier
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Trek name
    trek_name = db.Column(
        db.String(100),
        nullable=False
    )

    # Trek location
    location = db.Column(
        db.String(100),
        nullable=False
    )

    # Difficulty (Easy/Moderate/Hard)
    difficulty = db.Column(
        db.String(20),
        nullable=False
    )

    # Trek duration in days
    duration_days = db.Column(
        db.Integer,
        nullable=False
    )

    # Available slots for booking
    available_slots = db.Column(
        db.Integer,
        nullable=False
    )

    # Assigned staff id (references users table)
    assigned_staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    # Trek status
    status = db.Column(
        db.String(30),
        nullable=False
    )

    # Trek start date
    start_date = db.Column(
        db.Date,
        nullable=False
    )

    # Trek end date
    end_date = db.Column(
        db.Date,
        nullable=False
    )

    # Trek ki unna bookings access cheyyadaniki relationship
    bookings = db.relationship(
        "Booking",
        backref="trek",
        lazy=True
    )