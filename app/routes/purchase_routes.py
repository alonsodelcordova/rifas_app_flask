from flask import Blueprint, request, jsonify
from app.services.purchase_service import (
    reserve_numbers,
    confirm_payment
)
from app.decorators import role_required
from flask_login import login_required

purchase_bp = Blueprint("purchase", __name__, url_prefix="/purchases")


@purchase_bp.route("/my")
@login_required
@role_required("client", "admin")
def my_purchases():
    return "Mis compras"


@purchase_bp.route("/reserve", methods=["POST"])
def reserve():
    data = request.get_json()

    user_id = data.get("user_id")
    raffle_id = data.get("raffle_id")
    numbers = data.get("numbers")  # [12, 25, 30]

    if not all([user_id, raffle_id, numbers]):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        purchase = reserve_numbers(user_id, raffle_id, numbers)

        return jsonify({
            "message": "Números reservados",
            "purchase_id": purchase.id,
            "total": purchase.total_amount
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@purchase_bp.route("/<int:purchase_id>/confirm", methods=["POST"])
def confirm(purchase_id):
    try:
        confirm_payment(purchase_id)
        return jsonify({"message": "Pago confirmado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

from app.models import Purchase

@purchase_bp.route("/user/<int:user_id>", methods=["GET"])
def purchases_by_user(user_id):
    purchases = Purchase.query.filter_by(user_id=user_id).all()

    data = []
    for p in purchases:
        data.append({
            "id": p.id,
            "total": p.total_amount,
            "status": p.status,
            "created_at": p.created_at
        })

    return jsonify(data)
