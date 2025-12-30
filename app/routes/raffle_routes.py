from flask import Blueprint, jsonify, render_template
from app.models import Raffle, Winner, RaffleNumber, User

raffle_bp = Blueprint("raffle", __name__, url_prefix="/raffles")

@raffle_bp.route("/<int:raffle_id>/numbers")
def available_numbers(raffle_id):
    numbers = RaffleNumber.query.filter_by(
        raffle_id=raffle_id,
        status="available"
    ).all()

    return jsonify([n.number for n in numbers])

@raffle_bp.route("/<int:raffle_id>/winner")
def public_winner(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)

    winner = Winner.query.filter_by(raffle_id=raffle_id).first()

    if not winner:
        return render_template(
            "public/no_winner.html",
            raffle=raffle
        )

    number = RaffleNumber.query.get(winner.raffle_number_id)
    user = User.query.get(winner.user_id)

    return render_template(
        "public/winner.html",
        raffle=raffle,
        winner=winner,
        number=number,
        user=user
    )
