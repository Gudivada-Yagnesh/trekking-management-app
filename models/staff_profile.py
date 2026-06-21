# models package nunchi SQLAlchemy database object ni import chesthunam
from models import db


# Staff Profile table ni represent chese SQLAlchemy model
class StaffProfile(db.Model):

    # SQLite lo table name staff_profiles ani create avuthundhi
    __tablename__ = "staff_profiles"

    # Staff Profile unique identifier
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Users table lo unna id ni reference chesthundhi
    # One staff user ki one profile matrame undali kabatti unique=True
    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    # Staff contact details store chesthundhi
    contact_details = db.Column(
        db.String(255),
        nullable=False
    )