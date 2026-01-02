from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Payment
from flask_login import login_required  
from app.decorators import role_required
from app.models import RaffleNumber, Purchase, MetodoPayment
from datetime import datetime
from app.extensions import db
from flask import jsonify
from app.services.payments_service import list_payments, reallize_payment_service, confirm_payment_service

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/payments")
@login_required
def payments():
    payments = list_payments()
    return render_template("payments/payments.html", payments=payments)



@payment_bp.route("/payments/realize", methods=["POST"])
@login_required
def reallize_payment():
    purchase_id = request.form.get("purchase_id")
    method = request.form.get("method")
    amount = request.form.get("amount")
    reference_code = request.form.get("reference_code")

    if not method or not amount or not reference_code or not purchase_id:
        flash("Datos incompletos")
        return redirect(url_for("payments.payments"))
    
    data = reallize_payment_service(purchase_id, method, amount, reference_code)
    if data["success"]:
        flash(data["message"])
    else:
        flash(data["error"])
    return redirect(url_for("payments.payments"))
    



@payment_bp.route("/payments/<int:id>")
@login_required
def payment_detail(id):
    payment = Payment.query.get_or_404(id)
    return render_template(
        "payments/payment_detail.html",
        payment=payment
    )

@payment_bp.route("/payments/<int:payment_id>/confirm")
@login_required
@role_required("admin")
def confirm_payment_admin(payment_id):
    data = confirm_payment_service(payment_id)
    if data["success"]:
        flash(data["message"])
    else:
        flash(data["error"])
    return redirect(url_for("payments.payments"))


@payment_bp.route("/payments/<int:payment_id>/reject")
@login_required
@role_required("admin")
def reject_payment_admin(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    purchase = Purchase.query.get(payment.purchase_id)

    if payment.status != "pending":
        flash("Pago ya procesado")
        return redirect(url_for("payments.payments"))

    with db.session.begin():
        payment.status = "rejected"
        purchase.status = "cancelled"

        for item in purchase.items:
            rn = RaffleNumber.query.get(item.raffle_number_id)
            rn.status = "available"
            rn.reserved_at = None

    flash("Pago rechazado y números liberados")
    return redirect(url_for("payments.payments"))
