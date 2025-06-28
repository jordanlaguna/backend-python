from sqlalchemy.orm import Session
from app.models.model_sales import Sale
from app.schemas.schemas_sales import SaleRegister, SaleRegisterSuccess
from sqlalchemy.exc import SQLAlchemyError

def create_sale(db: Session, sale: SaleRegister):
    try:
        db_sale = Sale(
            sale_number=sale.sale_number,
            client_id=sale.client_id,
            user_id=sale.user_id,
            total=sale.total,
            subtotal=sale.subtotal,
            tax=sale.tax,
            payment_method=sale.payment_method,
            cash_received=sale.cash_received,
            change_given=sale.change_given,
            created_at=sale.created_at
        )
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
        return SaleRegisterSuccess(
            message="Venta registrada exitosamente",
            id_sale=db_sale.id
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise e  # o puedes lanzar HTTPException con detalle
