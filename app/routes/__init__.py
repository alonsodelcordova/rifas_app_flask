from .admin_routes import admin_blueprint
from .auth_routes import auth_blueprint
from .purchase_routes import purchase_bp
from .raffle_routes import raffle_bp
from .client_routes import client_bp
from .seller_routes import seller_bp
from flask import Flask

def register_blueprints(app: Flask):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(raffle_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(seller_bp)
