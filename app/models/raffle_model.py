from app.extensions import db
from datetime import datetime

class EstadoRaffle:
    draft = "draft"
    active = "active"
    finished = "finished"
    cancelled = "cancelled"

class Raffle(db.Model):
    __tablename__ = "raffles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price_per_number = db.Column(db.Float, nullable=False)
    total_numbers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default=EstadoRaffle.draft)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    numbers = db.relationship("RaffleNumber", backref="raffle", lazy=True)
