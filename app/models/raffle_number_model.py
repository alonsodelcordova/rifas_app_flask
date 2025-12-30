from app.extensions import db
from datetime import datetime

class EstadoRaffleNumber:
    available = "available"
    reserved = "reserved"
    sold = "sold"

class RaffleNumber(db.Model):
    __tablename__ = "raffle_numbers"

    id = db.Column(db.Integer, primary_key=True)
    raffle_id = db.Column(db.Integer, db.ForeignKey("raffles.id"))
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default=EstadoRaffleNumber.available)

    reserved_at = db.Column(db.DateTime)
    sold_at = db.Column(db.DateTime)

    purchase_item = db.relationship(
        "PurchaseItem",
        back_populates="raffle_number",
        uselist=False
    )

    __table_args__ = (
        db.UniqueConstraint("raffle_id", "number", name="uq_raffle_number"),
    )
