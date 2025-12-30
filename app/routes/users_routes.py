
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import User, RolUsuario
from flask_login import login_required
import bcrypt
from datetime import datetime
from app.decorators import role_required
from flask import send_from_directory
from app.services.admin_service import get_seller_stats, get_admin_stats

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/users")
@login_required
@role_required("admin")
def users():
    users = User.query.all()
    return render_template("users/users.html", users=users)