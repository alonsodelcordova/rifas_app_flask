from app.extensions import db
from datetime import datetime


class RolUsuario:
    client = "client"
    seller = "seller"
    admin = "admin"
    
    def values():
        return [
            RolUsuario.client,
            RolUsuario.seller,
            RolUsuario.admin
        ]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default=RolUsuario.client)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def get_id(self):
        return self.id
    
    @property
    def is_authenticated(self):
        return self.is_active