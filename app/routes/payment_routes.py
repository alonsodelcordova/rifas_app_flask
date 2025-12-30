from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Payment
from flask_login import login_required  
from app.decorators import role_required
from app.services.purchase_service import Purchase
from app.models import RaffleNumber
from datetime import datetime
from app.extensions import db

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/payments")
@login_required
@role_required("admin")
def payments():
    payments = Payment.query.filter_by(status="pending").all()
    return render_template("admin/payments.html", payments=payments)



@payment_bp.route("/payments/<int:id>")
@login_required
def payment_detail(id):
    payment = Payment.query.get_or_404(id)
    return render_template(
        "client/payment_detail.html",
        payment=payment
    )

@payment_bp.route("/payments/<int:payment_id>/confirm")
@login_required
@role_required("admin")
def confirm_payment_admin(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    purchase = Purchase.query.get(payment.purchase_id)

    if payment.status != "pending":
        flash("Pago ya procesado")
        return redirect(url_for("payments.payments"))

    with db.session.begin():
        payment.status = "confirmed"
        payment.paid_at = datetime.utcnow()

        purchase.status = "paid"

        for item in purchase.items:
            rn = RaffleNumber.query.get(item.raffle_number_id)
            rn.status = "sold"
            rn.sold_at = datetime.utcnow()

    flash("Pago confirmado correctamente")
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

@payment_bp.route("/payments/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def new_payment():
    if request.method == "POST":
        method = request.form["method"]
        amount = request.form["amount"]
        reference_code = request.form["reference_code"]

        if not method or not amount or not reference_code:
            flash("Datos incompletos")
            return redirect(url_for("payments.payments"))
        try:
            amount = float(amount)
        except ValueError:
            flash("Monto no válido")
            return redirect(url_for("payments.payments"))

        with db.session.begin():
            payment = Payment(
                purchase_id=None,
                method=method,
                amount=amount,
                reference_code=reference_code,
                status="pending"
            )
            db.session.add(payment)
            db.session.commit()

            flash("Pago creado correctamente")
            return redirect(url_for("payments.payments"))
    else:
        return render_template("admin/new_payment.html")


