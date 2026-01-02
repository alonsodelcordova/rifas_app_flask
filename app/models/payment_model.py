from app.extensions import db
from datetime import datetime

class MetodoPayment:
    cash = "cash"
    yape = "yape"
    card = "card"
    transfer = "transfer"
    
    def values():
        return [
            MetodoPayment.yape,
            MetodoPayment.cash,
            MetodoPayment.card,
            MetodoPayment.transfer
        ]

class EstadoPayment:
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchases.id"))
    method = db.Column(db.String(30), default=MetodoPayment.cash)
    amount = db.Column(db.Float)
    reference_code = db.Column(db.String(100))
    status = db.Column(db.String(20), default=EstadoPayment.pending)
    paid_at = db.Column(db.DateTime)
    
    purchase = db.relationship("Purchase", backref="payments", uselist=False)
    
    
