import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "s3cr34y_90")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///db.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False