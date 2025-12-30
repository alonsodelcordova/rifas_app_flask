from flask import Flask
from .extensions import db, migrate, login_manager, bcrypt
from .config import Config
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import register_blueprints
    register_blueprints(app)

    return app