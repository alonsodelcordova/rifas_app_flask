
from app.extensions import db
from app.models import User

def get_users():
    return User.query.all()

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


