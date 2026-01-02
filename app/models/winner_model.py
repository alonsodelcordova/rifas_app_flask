from app.extensions import db
from datetime import datetime

class Winner(db.Model):
    __tablename__ = "winners"

    id = db.Column(db.Integer, primary_key=True)
    raffle_id = db.Column(db.Integer, db.ForeignKey("raffles.id"))
    raffle_number_id = db.Column(
        db.Integer, db.ForeignKey("raffle_numbers.id")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    seed = db.Column(db.String(100))
    drawn_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    raffle = db.relationship(
        "Raffle",
        backref="winner",
        uselist=False
    )
    raffle_number = db.relationship(
        "RaffleNumber",
        backref="winner",
        uselist=False
    )
    
    user = db.relationship(
        "User",
        backref="winner",
        uselist=False
    )
