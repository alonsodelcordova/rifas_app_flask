from app.extensions import db
from datetime import datetime

class EstadoPurchase:
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"
    

# compra de numeros
class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    raffle_id = db.Column(db.Integer, db.ForeignKey("raffles.id"))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default=EstadoPurchase.pending)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("PurchaseItem", backref="purchase", lazy=True)
    user = db.relationship("User", backref="purchases", uselist=False)
    raffle = db.relationship("Raffle", backref="purchases", uselist=False)

    @property
    def total_numbers(self):
        return [item.raffle_number.number for item in self.items]

class PurchaseItem(db.Model):
    __tablename__ = "purchase_items"

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchases.id"))
    raffle_number_id = db.Column(
        db.Integer, db.ForeignKey("raffle_numbers.id")
    )
    price = db.Column(db.Float)

    raffle_number = db.relationship(
        "RaffleNumber",
        back_populates="purchase_item",
        uselist=False
    )

