from flask import Blueprint, jsonify, render_template, flash, request, redirect, url_for
from app.models import Raffle, Winner, RaffleNumber, User, EstadoRaffleNumber
from app.services.raffles_service import get_active_raffles_cliente, get_raffle_detail, activate_raffle, delete_raffle
from app.services.purchase_service import buy_numbers
from flask_login import login_required, current_user
from app.decorators import role_required
from app.services.raffles_service import create_raffle
from app.services.pdf_service import generate_raffle_pdf
from app.services.raffles_service import draw_raffle
from flask import send_from_directory

raffle_bp = Blueprint("raffles", __name__, url_prefix="/raffles")


# consulta de rifas
@raffle_bp.route("/raffles")
def raffles():
    raffles = []
    if current_user.role == "client":
        raffles = get_active_raffles_cliente()
    elif current_user.role == "admin":
        raffles = Raffle.query.all()

    return render_template(
        "raffles/raffles.html",
        raffles=raffles
    )
    
# creación de rifa
@raffle_bp.route("/raffles/create", methods=["GET", "POST"])
@login_required
@role_required("seller","admin")
def create():
    if request.method == "POST":
        data = request.form
        title = request.form["title"]
        price_per_number = request.form["price_per_number"]
        total_numbers = request.form["total_numbers"]
        description = request.form["description"]
        if not title or not price_per_number or not total_numbers:
            flash("Datos incompletos")
            return redirect(url_for("raffles.create"))
        message = create_raffle(
            title = title,
            price_per_number = float(price_per_number),
            total_numbers = int(total_numbers),
            description = description
        )
        flash(message)
        return redirect(url_for("raffles.raffles"))
    return render_template("raffles/create_raffle.html")

# activar rifa para que los clientes puedan comprar
@raffle_bp.route("/<int:raffle_id>/activate", methods=["GET"])
@login_required
@role_required("admin")
def activate_raffle_admin(raffle_id):
    raffle = activate_raffle(raffle_id)
    flash("Rifa activada correctamente")
    return redirect(url_for("raffles.raffles"))

# eliminar rifa
@raffle_bp.route("/<int:raffle_id>/delete", methods=["GET"])
@login_required
@role_required("admin")
def delete_raffle_admin(raffle_id):
    data = delete_raffle(raffle_id)
    flash(data["message"])
    return redirect(url_for("raffles.raffles"))


# detalle de rifa
@raffle_bp.route("/raffles/<int:raffle_id>")
def raffle_detail(raffle_id):
    
    return render_template(
        "raffles/raffle_detail.html",
        raffle=get_raffle_detail(raffle_id)
    )
    


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
