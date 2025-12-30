
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User, Raffle, RaffleNumber, Payment, Purchase, Winner
from flask_login import current_user, login_required
import bcrypt
from datetime import datetime
from app.decorators import role_required
from flask import send_from_directory
from app.services.admin_service import get_seller_stats, get_admin_stats

admin_blueprint = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)

@admin_blueprint.route("/dashboard")
@login_required
def dashboard():
    role = current_user.role
    if role == "client":
        return render_template("dashboard/client_dashboard.html")
    elif role == "seller":
        stats = get_seller_stats()
        return render_template("dashboard/seller_dashboard.html", stats=stats)
    else:
        stats = get_admin_stats()
        return render_template("dashboard/admin_dashboard.html", stats=stats)


@admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin():
    if not current_user.is_admin:
        flash('No tienes permisos de administrador')
        return redirect(url_for('auth.index'))
    else:
        return render_template('admin.html')
    



@admin_blueprint.route("/descargar/<string:filename>")
@login_required
def descargar(filename):
    return send_from_directory(
        "static/pdfs",
        filename,
        as_attachment=True
    )


@admin_blueprint.route("/dashboard_seler")
@login_required
@role_required("seller")
def dashboard_seller():
    return render_template(
        "seller/dashboard.html",
        stats= get_seller_stats()
    )
