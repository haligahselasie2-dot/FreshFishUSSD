import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "data.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_QR = os.path.join(BASE_DIR, "static", "qr")
