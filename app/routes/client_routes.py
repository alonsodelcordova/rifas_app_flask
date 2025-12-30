from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.client_service import get_active_raffles, get_raffle_detail, get_my_purchases
from app.services.purchase_service import buy_numbers

client_bp = Blueprint("client", __name__, url_prefix="/client")


@client_bp.route("/")
def inicio():
    return render_template("client/index.html")

@client_bp.route("/raffles")
def raffles():
    return render_template(
        "client/raffles.html",
        raffles=get_active_raffles()
    )

@client_bp.route("/raffles/<int:raffle_id>")
def raffle_detail(raffle_id):
    return render_template(
        "client/raffle_detail.html",
        raffle=get_raffle_detail(raffle_id)
    )

@client_bp.route("/raffles/<int:raffle_id>/buy", methods=["POST"])
@login_required
def buy(raffle_id):
    numbers = request.form.getlist("numbers")
    try:
        buy_numbers(raffle_id, numbers)
        flash("Compra realizada")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("client.raffle_detail", raffle_id=raffle_id))


@client_bp.route("/my-purchases")
@login_required
def my_purchases():
    return render_template(
        "client/my_purchases.html",
        purchases=get_my_purchases()
    )

