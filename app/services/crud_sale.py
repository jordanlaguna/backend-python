from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.model_sales import Sale
from app.models.model_product import Product
from app.schemas.schemas_sales import SaleRegister, SaleRegisterSuccess

def create_sale(db: Session, sale: SaleRegister):
    try:
        # verify if the sale number already exists
        for item in sale.products:
            product = db.query(Product).filter(Product.id_product == item.product_id).first()
            if not product:
                raise ValueError(f"Producto con ID {item.product_id} no existe.")
            if product.stock < item.quantity:
                raise ValueError(f"Stock insuficiente para el producto '{product.name}'. Disponible: {product.stock}, solicitado: {item.quantity}")

            product.stock -= item.quantity

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
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise e 
    except Exception as e:
        db.rollback()
        raise SQLAlchemyError(f"Error al registrar la venta: {str(e)}")
    finally:
        db.close()
