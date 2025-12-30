from flask import Blueprint, jsonify, render_template, flash, request, redirect, url_for
from app.models import Raffle, Winner, RaffleNumber, User, EstadoRaffleNumber
from app.services.raffles_service import get_active_raffles, get_raffle_detail, get_my_purchases
from app.services.purchase_service import buy_numbers
from flask_login import login_required, current_user
from app.decorators import role_required
from app.services.raffles_service import create_raffle
from app.services.pdf_service import generate_raffle_pdf
from app.services.raffles_service import draw_raffle
from flask import send_from_directory

raffle_bp = Blueprint("raffles", __name__, url_prefix="/raffles")

@raffle_bp.route("/raffles")
def raffles():
    raffles = []
    if current_user.role == "client":
        raffles = get_active_raffles()
    elif current_user.role == "admin":
        raffles = Raffle.query.all()

    return render_template(
        "raffles/raffles.html",
        raffles=raffles
    )
    
@raffle_bp.route("/raffles/create", methods=["GET", "POST"])
@login_required
@role_required("seller","admin")
def create():
    if request.method == "POST":
        data = request.form
        if not data["total_numbers"] or not data["price_per_number"]:
            flash("Datos incompletos")
            return redirect(url_for("raffles.create"))
        create_raffle(request.form)
        flash("Rifa creada")
        return redirect(url_for("raffles.raffles"))
    return render_template("raffles/create_raffle.html")



@raffle_bp.route("/<int:raffle_id>/numbers")
def available_numbers(raffle_id):
    numbers = RaffleNumber.query.filter_by(
        raffle_id=raffle_id,
        status=EstadoRaffleNumber.available
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

@raffle_bp.route("/raffles/<int:raffle_id>")
def raffle_detail(raffle_id):
    return render_template(
        "client/raffle_detail.html",
        raffle=get_raffle_detail(raffle_id)
    )

@raffle_bp.route("/raffles/<int:raffle_id>/buy", methods=["POST"])
@login_required
def buy(raffle_id):
    numbers = request.form.getlist("numbers")
    try:
        buy_numbers(raffle_id, numbers)
        flash("Compra realizada")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("raffles.raffle_detail", raffle_id=raffle_id))


@raffle_bp.route("/raffles/<int:raffle_id>/draw")
@login_required
@role_required("admin")
def draw_raffle_admin(raffle_id):
    try:
        winner = draw_raffle(raffle_id)
        flash("Sorteo realizado correctamente")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("raffles.raffles"))



@raffle_bp.route("/raffles/<int:raffle_id>/acta")
@login_required
@role_required("admin")
def download_acta(raffle_id):
    raffle = Raffle.query.get_or_404(raffle_id)
    winner = Winner.query.filter_by(raffle_id=raffle_id).first_or_404()

    number = RaffleNumber.query.get(winner.raffle_number_id)
    user = User.query.get(winner.user_id)

    filename = generate_raffle_pdf(raffle, winner, user, number)

    return send_from_directory(
        "static/pdfs",
        filename,
        as_attachment=True
    )
