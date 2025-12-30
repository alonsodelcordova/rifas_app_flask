from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.decorators import role_required
from app.services.seller_service import *

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")

@seller_bp.route("/dashboard")
@login_required
@role_required("seller")
def dashboard():
    return render_template(
        "seller/dashboard.html",
        stats= get_seller_stats()
    )

@seller_bp.route("/raffles/create", methods=["GET", "POST"])
@login_required
@role_required("seller")
def create():
    if request.method == "POST":
        create_raffle(request.form)
        flash("Rifa creada")
        return redirect(url_for("seller.dashboard"))

    return render_template("seller/create_raffle.html")
