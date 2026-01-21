
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.decorators import role_required
from app.services.users_service import get_users, get_user_detail, eliminar_usuario, crear_usuario
from app.models import RolUsuario

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/users")
@login_required
@role_required("admin")
def users():
    users = get_users()
    return render_template("users/users.html", users=users)

@users_bp.route("/users/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def new_user():
    if request.method == "POST":
        if username == "" or password == "":
            flash("Falta campo", "error")
            return redirect(url_for("users.new_user"))
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        data = crear_usuario(username, password, role)
        flash(data["message"])
        return redirect(url_for("users.users"))
    else:
        roles = RolUsuario.values()
        return render_template("users/new_user.html", roles=roles)

@users_bp.route("/users/<int:id>")
@login_required
@role_required("admin")
def user_detail(id):
    user = get_user_detail(id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.users"))
    data = eliminar_usuario(id)
    flash(data["message"], "success")
    return redirect(url_for("users.users"))
    