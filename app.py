from flask import Flask
from config import Config
from models import db
from models.user import User
from models.staff_profile import StaffProfile
from models.trek import Trek
from models.booking import Booking
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app) #sqlalchemy


# Application context create chesthunam
with app.app_context():

    # Models prakaram SQLite tables create chesthundhi
    db.create_all()

    # Admin user already undho ledho check chesthunam
    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    # Admin lekapothe create chestham
    if admin is None:

        # Admin object create chesthunam
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="ADMIN",
            status="ACTIVE"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created successfully.")

    else:

        print("Admin user already exists.")


if __name__ == "__main__":
    app.run(debug=True)