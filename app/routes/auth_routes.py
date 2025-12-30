

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db, bcrypt
from app.models import User, RolUsuario
from flask_login import login_user, logout_user, login_required
import json

auth_blueprint = Blueprint(
    "auth",
    __name__
)


@auth_blueprint.route('/')
def index():
    return render_template('index.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            user.is_active = True
            is_login = login_user(user)
            if not  is_login:
                flash('Invalid username or password')
                return redirect(url_for('auth.index'))
            
            if user.role == RolUsuario.client:
                return redirect(url_for('client.inicio'))
            elif user.role == RolUsuario.seller:
                return redirect(url_for('seller.dashboard'))
            else:
                return redirect(url_for('admin.dashboard'))

            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('auth/login.html', error='Invalid username or password')
    else:
        return render_template('auth/login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return render_template('register.html', error='Username already exists')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registro exitoso')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')



@auth_blueprint.route('/api/login', methods=['GET', 'POST'])
def api_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            return json.dumps({'success': True})
        else:
            return json.dumps({'success': False})
    else:
        return json.dumps({'success': False})