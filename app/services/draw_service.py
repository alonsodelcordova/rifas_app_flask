import random
from datetime import datetime
from app.extensions import db
from app.models import Raffle, RaffleNumber, Winner

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

        raffle.status = "finished"
        db.session.add(winner)

    return winner
