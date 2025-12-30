from .admin_routes import admin_blueprint
from .auth_routes import auth_blueprint
from .payment_routes import payment_bp
from .purchase_routes import purchase_bp
from .raffle_routes import raffle_bp
from .users_routes import users_bp
from flask import Flask

def register_blueprints(app: Flask):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(payment_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(raffle_bp)
    app.register_blueprint(users_bp)
