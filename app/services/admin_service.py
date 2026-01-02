from app.extensions import db
from app.models import Raffle, EstadoRaffle, RaffleNumber, Payment, User, RolUsuario, Winner
from flask_login import current_user

def get_admin_stats():
    active_raffles = Raffle.query.filter_by(status="active").count()
    sold_numbers = RaffleNumber.query.filter_by(status="sold").count()
    total_income = db.session.query(
        db.func.sum(Payment.amount)
    ).filter_by(status="confirmed").scalar() or 0
    users = User.query.count()
    return {
        "active_raffles": active_raffles,
        "sold_numbers": sold_numbers,
        "total_income": total_income,
        "users": users
    }

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

def get_client_stats():
    id_client = current_user.id
    raffles = Raffle.query.filter_by(status="active").all()
    sold_numbers = RaffleNumber.query.filter_by(
            status="sold", client_id=id_client
        ).count()
    pending_numbers = RaffleNumber.query.filter_by(
            status="reserved", client_id=id_client
        ).count()
    
    winners = Winner.query.filter_by(user_id=id_client).all()
    
    return {
        "active_raffles": len(raffles),
        "sold_numbers": sold_numbers,
        "pending_numbers": pending_numbers,
        "winners": winners
    }