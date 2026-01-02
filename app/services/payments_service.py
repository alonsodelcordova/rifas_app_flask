
from app.extensions import db
from app.models import Payment, Purchase, EstadoPurchase, EstadoPayment, EstadoRaffleNumber
from flask_login import current_user
from datetime import datetime

def list_payments():
    if current_user.role == "admin":
        pagos = Payment.query.all()
    elif current_user.role == "client":
        
        pagos = Payment.query.join(Purchase).filter(
            Purchase.user_id == current_user.id
        ).all()
    else:
        pagos = []
        
    return pagos

def reallize_payment_service(purchase_id, method, amount, reference_code):
    purchase = Purchase.query.get_or_404(purchase_id)
    if purchase.status != EstadoPurchase.pending:
        return {
            "error": "Compra inválida",
            "success": False
        }
    if purchase.user_id != current_user.id:
        return {
            "error": "No tienes permisos para realizar este pago",
            "success": False
        }
    
    if float(amount) != float(purchase.total_amount):
        return {
            "error": "Monto no válido, debe ser igual al total",
            "success": False
        }
    
    try:
        
        payment = Payment(
            purchase_id=purchase_id,
            method=method,
            amount=amount,
            reference_code=reference_code,
            status=EstadoPayment.pending,
            paid_at=datetime.utcnow()
        )
        db.session.add(payment)
        db.session.commit()
        
        return {
            "message": "Pago realizado correctamente",
            "success": True
        }
    except Exception as e:
        db.session.rollback()
        return {
            "error": str(e),
            "success": False
        }

    
def confirm_payment_service(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    if payment.status != EstadoPayment.pending:
        return {
            "error": "Pago inválido",
            "success": False
        }
    
    if payment.purchase.status != EstadoPurchase.pending:
        return {
            "error": "Compra inválida",
            "success": False
        }

    payment.status = EstadoPayment.confirmed
    payment.purchase.status = EstadoPurchase.paid
    
    for item in payment.purchase.items:
        item.raffle_number.status = EstadoRaffleNumber.sold
        item.raffle_number.sold_at = datetime.utcnow()
    db.session.commit()
    
    return {
        "message": "Pago confirmado correctamente",
        "success": True
    }



