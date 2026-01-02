from datetime import datetime, timedelta
from app.extensions import db
from app.models import (
    RaffleNumber, 
    Purchase, 
    PurchaseItem, 
    EstadoRaffleNumber,
    EstadoPurchase
)
from flask_login import current_user

RESERVE_MINUTES = 10

def reserve_numbers(user_id, raffle_id, numbers):
    """
    Reserva de números (TRANSACCIÓN) <br>
    - bloquea las filas mientras dura la transacción
    - otro usuario no puede tocarlas <br>
    :param user_id: usuario que realiza la reserva
    :param raffle_id: id del sorteo
    :param numbers: lista de números a reservar
    """
    try:

        raffle_numbers = (
            db.session.query(RaffleNumber)
            .filter(
                RaffleNumber.raffle_id == raffle_id,
                RaffleNumber.number.in_(numbers),
                RaffleNumber.status == EstadoRaffleNumber.available,
            )
            .with_for_update()  # BLOQUEO 
            .all()
        )

        if len(raffle_numbers) != len(numbers):
            print("Algunos números ya no están disponibles")
            raise Exception("Algunos números ya no están disponibles")

        # Crear compra
        purchase = Purchase(
            user_id=user_id,
            raffle_id=raffle_id,
            status=EstadoPurchase.pending
        )
        db.session.add(purchase)
        db.session.flush()

        total = 0

        for rn in raffle_numbers:
            rn.status = EstadoRaffleNumber.reserved
            rn.reserved_at = datetime.utcnow()
            rn.client_id = user_id
            item = PurchaseItem(
                purchase_id=purchase.id,
                raffle_number_id=rn.id,
                price=rn.raffle.price_per_number
            )
            db.session.add(item)
            total += item.price

        purchase.total_amount = total
        db.session.commit()
        return purchase

    except Exception as e:
        db.session.rollback()
        print(e)
        raise e

def confirm_payment(purchase_id):
    """
        Confirmación de pago <br>
        Cuando el admin confirma el pago (o webhook):
    """
    with db.session.begin():
        purchase = Purchase.query.get_or_404(purchase_id)

        if purchase.status != EstadoPurchase.pending:
            raise Exception("Compra inválida")

        purchase.status = EstadoPurchase.paid

        for item in purchase.items:
            rn = RaffleNumber.query.get(item.raffle_number_id)
            rn.status = EstadoRaffleNumber.sold
            rn.sold_at = datetime.utcnow()


def release_expired_reservations():
    """
        Liberar reservas vencidas (JOB)
    """
    expiration_time = datetime.utcnow() - timedelta(minutes=RESERVE_MINUTES)

    expired = RaffleNumber.query.filter(
        RaffleNumber.status == EstadoRaffleNumber.reserved,
        RaffleNumber.reserved_at < expiration_time
    ).all()

    for rn in expired:
        rn.status = EstadoRaffleNumber.available
        rn.reserved_at = None

    db.session.commit()


# TODO: Comprobar que no haya compras pendientes
def buy_numbers(raffle_id, number):
    print(f"comprando números {number}")
    try:
        purchase = Purchase(
            user_id=current_user.id,
            raffle_id=raffle_id,
            status=EstadoPurchase.pending
        )
        db.session.add(purchase)
        db.session.flush()

        raffle_number = RaffleNumber.query.filter_by(
            raffle_id=raffle_id,
            number=number,
            status=EstadoRaffleNumber.available
        ).with_for_update().first()

        if not raffle_number:
            return "Número no disponible"

        raffle_number.status = EstadoRaffleNumber.reserved

        item = PurchaseItem(
            purchase=purchase,
            raffle_number=raffle_number
        )
        db.session.add(item)
        db.session.commit()
        return "Compra realizada"
    except Exception as e:
        db.session.rollback()
        print(e)
        return "Error al comprar: " + str(e)

def get_my_purchases():
    if current_user.role == "client":
        return Purchase.query.filter_by(user_id=current_user.id).all()
    elif current_user.role == "admin":
        return Purchase.query.all()
    else:
        return []
