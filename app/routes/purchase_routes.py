from flask import Blueprint, request, jsonify, render_template
from app.services.purchase_service import (
    reserve_numbers,
    confirm_payment,
    get_my_purchases
)
from app.decorators import role_required
from flask_login import login_required, current_user
from app.models import MetodoPayment, Purchase

purchase_bp = Blueprint("purchase", __name__, url_prefix="/purchases")


@purchase_bp.route("/purchases")
@login_required
@role_required("client", "admin")
def purchases():
    return render_template(
        "purchases/purchases.html",
        purchases=get_my_purchases()
    )

# reservar números
@purchase_bp.route("/reserve", methods=["POST"])
@login_required
def reserve():
    data = request.get_json()

    raffle_id = data.get("raffle_id")
    numbers = data.get("numbers")  # [12, 25, 30]

    if not all([raffle_id, numbers]):
        return jsonify({"error": "Datos incompletos"}), 400
    user_id = current_user.id
    try:
        purchase = reserve_numbers(user_id, raffle_id, numbers)

        return jsonify({
            "message": "Números reservados",
            "purchase_id": purchase.id,
            "total": purchase.total_amount,
            "success": True
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


@purchase_bp.route("/purchases/<int:purchase_id>")
def purchase_detail(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    
    metodos_pagos = MetodoPayment.values()

    return render_template(
        "purchases/purchase_detail.html",
        purchase=purchase,
        metodos_pagos=metodos_pagos
    )