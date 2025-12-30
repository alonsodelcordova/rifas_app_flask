from app.models import Raffle, Purchase, EstadoRaffle
from flask_login import current_user

def get_active_raffles():
    return Raffle.query.filter_by(status=EstadoRaffle.active).all()

def get_raffle_detail(raffle_id):
    return Raffle.query.get_or_404(raffle_id)

def get_my_purchases():
    return Purchase.query.filter_by(user_id=current_user.id).all()
