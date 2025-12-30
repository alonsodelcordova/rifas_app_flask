
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User, Raffle, RaffleNumber, Payment, Purchase, Winner
from flask_login import current_user, login_required
import bcrypt
from datetime import datetime
from app.decorators import role_required
from app.services.draw_service import draw_raffle
from app.services.pdf_service import generate_raffle_pdf
from flask import send_from_directory

admin_blueprint = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@role_required("admin")
def admin():
    if not current_user.is_admin:
        flash('No tienes permisos de administrador')
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            user.is_admin = True
            db.session.commit()
            return redirect(url_for('admin.admin'))
        else:
            return render_template('admin.html', error='Invalid username or password')
    else:
        return render_template('admin.html')
    
@admin_blueprint.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = {
        "active_raffles": Raffle.query.filter_by(status="active").count(),
        "sold_numbers": RaffleNumber.query.filter_by(status="sold").count(),
        "total_income": db.session.query(
            db.func.sum(Payment.amount)
        ).scalar() or 0,
        "users": User.query.count()
    }

    return render_template("admin/dashboard.html", stats=stats)

@admin_blueprint.route("/raffles")
@login_required
@role_required("admin")
def raffles():
    raffles = Raffle.query.all()
    return render_template("admin/raffles.html", raffles=raffles)




@admin_blueprint.route("/users")
@login_required
@role_required("admin")
def users():
    users = User.query.all()
    return render_template("admin/users.html", users=users)

@admin_blueprint.route("/payments")
@login_required
@role_required("admin")
def payments():
    payments = Payment.query.filter_by(status="pending").all()
    return render_template("admin/payments.html", payments=payments)

@admin_blueprint.route("/payments/<int:payment_id>/confirm")
@login_required
@role_required("admin")
def confirm_payment_admin(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    purchase = Purchase.query.get(payment.purchase_id)

    if payment.status != "pending":
        flash("Pago ya procesado")
        return redirect(url_for("admin.payments"))

    with db.session.begin():
        payment.status = "confirmed"
        payment.paid_at = datetime.utcnow()

        purchase.status = "paid"

        for item in purchase.items:
            rn = RaffleNumber.query.get(item.raffle_number_id)
            rn.status = "sold"
            rn.sold_at = datetime.utcnow()

    flash("Pago confirmado correctamente")
    return redirect(url_for("admin.payments"))


@admin_blueprint.route("/payments/<int:payment_id>/reject")
@login_required
@role_required("admin")
def reject_payment_admin(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    purchase = Purchase.query.get(payment.purchase_id)

    if payment.status != "pending":
        flash("Pago ya procesado")
        return redirect(url_for("admin.payments"))

    with db.session.begin():
        payment.status = "rejected"
        purchase.status = "cancelled"

        for item in purchase.items:
            rn = RaffleNumber.query.get(item.raffle_number_id)
            rn.status = "available"
            rn.reserved_at = None

    flash("Pago rechazado y números liberados")
    return redirect(url_for("admin.payments"))

@admin_blueprint.route("/payments/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def new_payment():
    if request.method == "POST":
        method = request.form["method"]
        amount = request.form["amount"]
        reference_code = request.form["reference_code"]

        if not method or not amount or not reference_code:
            flash("Datos incompletos")
            return redirect(url_for("admin.payments"))

        try:
            amount = float(amount)
        except ValueError:
            flash("Monto no válido")
            return redirect(url_for("admin.payments"))

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
            return redirect(url_for("admin.payments"))
    else:
        return render_template("admin/new_payment.html")


@admin_blueprint.route("/raffles/<int:raffle_id>/draw")
@login_required
@role_required("admin")
def draw_raffle_admin(raffle_id):
    try:
        winner = draw_raffle(raffle_id)
        flash("Sorteo realizado correctamente")
    except Exception as e:
        flash(str(e))

    return redirect(url_for("admin.raffles"))



@admin_blueprint.route("/raffles/<int:raffle_id>/acta")
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


@admin_blueprint.route("/descargar/<string:filename>")
@login_required
def descargar(filename):
    return send_from_directory(
        "static/pdfs",
        filename,
        as_attachment=True
    )