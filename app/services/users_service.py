
from app.extensions import db
from app.models import User
import bcrypt

def get_users():
    return User.query.all()


def get_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return user

def crear_usuario(username, password, role):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return {
            "message": "El usuario ya existe"
        }
    
    try:
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    except Exception as e:
        return {
            "message": str(e)
        }

    user = User(
        username=username,
        password=password,
        role=role,
        is_admin=False
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "Usuario creado correctamente"
    }

def eliminar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {
        "message": "Usuario eliminado correctamente"
    }

def deshabilitar_usuario(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return {
        "message": "Usuario deshabilitado correctamente"
    }


