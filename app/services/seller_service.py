from app.extensions import db
from app.models import Raffle, EstadoRaffle, RaffleNumber, Payment, User, RolUsuario
from flask_login import current_user

def create_raffle(data):
    raffle = Raffle(
        title=data["title"],
        price=data["price"],
        total_numbers=data["total_numbers"],
        seller_id=current_user.id,
        status=EstadoRaffle.draft
    )
    db.session.add(raffle)
    db.session.commit()
    return raffle

def get_my_raffles():
    return Raffle.query.filter_by(created_by=current_user.id).all()

def get_seller_stats():
    rafles_count = Raffle.query.filter_by(created_by=current_user.id).count()
    sold_numbers = 0
    if rafles_count > 0:
        sold_numbers = RaffleNumber.query.filter_by(
            raffle_id=Raffle.query.filter_by(created_by=current_user.id).first().id,
            status="sold"
        ).count()
    
    stats = {
        "raffles": rafles_count,
        "sold_numbers": sold_numbers,
        "total_income": db.session.query(
            db.func.sum(Payment.amount)
        ).scalar() or 0,
        "clients": User.query.filter_by(role = RolUsuario.client).count()
    }

    return stats
