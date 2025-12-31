import random
from datetime import datetime
from app.extensions import db
from app.models import Raffle, RaffleNumber, Winner, Purchase, EstadoRaffle, EstadoRaffleNumber
from flask_login import current_user

def get_active_raffles_cliente():
    
    return Raffle.query.filter_by(status=EstadoRaffle.active).all()

def get_raffle_detail(raffle_id):
    return Raffle.query.get_or_404(raffle_id)

def get_my_purchases():
    return Purchase.query.filter_by(user_id=current_user.id).all()

# realizar sorteo
def draw_raffle(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)

    if raffle.status != "active":
        raise Exception("La rifa no está activa")

    sold_numbers = RaffleNumber.query.filter_by(
        raffle_id=raffle_id,
        status="sold"
    ).all()

    if not sold_numbers:
        raise Exception("No hay números vendidos")

    # 🔑 Seed transparente
    seed = f"RIFA-{raffle_id}-{datetime.utcnow().date()}-{len(sold_numbers)}"
    random.seed(seed)

    winner_number = random.choice(sold_numbers)
    with db.session.begin():
        winner = Winner(
            raffle_id=raffle_id,
            raffle_number_id=winner_number.id,
            user_id=winner_number.purchase_item.purchase.user_id,
            seed=seed,
            drawn_at=datetime.utcnow()
        )

        raffle.status = EstadoRaffle.finished
        db.session.add(winner)

    return winner

# crear nuevo sorteo
def create_raffle(
    title: str,
    price_per_number: float,
    total_numbers: int,
    description: str,
):
    if not title or not price_per_number or not total_numbers:
        return "Datos incompletos"
    
    try:
        raffle = Raffle(
            title=title,
            price_per_number=price_per_number,
            total_numbers=total_numbers,
            created_by=current_user.id,
            status=EstadoRaffle.draft,
            description=description
        )
        db.session.add(raffle)
        db.session.flush()
        raffleNumbers = []
        for i in range(total_numbers):
            raffleNumber = RaffleNumber(
                raffle_id=raffle.id,
                number=i+1,
                status=EstadoRaffleNumber.available
            )
            raffleNumbers.append(raffleNumber)
        db.session.bulk_save_objects(raffleNumbers)
        db.session.commit()
        return "Rifa creada"
    except Exception as e:
        db.session.rollback()
        return str(e)


def get_my_raffles():
    return Raffle.query.filter_by(created_by=current_user.id).all()

def activate_raffle(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)
    raffle.status = "active"
    db.session.commit()
    return raffle


def delete_raffle(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)
    db.session.delete(raffle)
    db.session.commit()
    return {
        "message": "Rifa eliminada correctamente"
    }