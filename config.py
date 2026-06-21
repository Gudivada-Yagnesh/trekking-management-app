import os

# Ee file (config.py) unna folder absolute path ni store chesthundhi
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "trekking-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR,
        "instance",
        "trekking.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False