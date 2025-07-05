from sqlalchemy.orm import Session
from app.models.model_sales import Sale
from app.models.model_product import Product
from app.models.model_sale_details import SaleDetail
from app.schemas.schemas_sales import SaleRegister, SaleRegisterSuccess
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def create_sale(db: Session, sale: SaleRegister):
    try:
        # create a new sale record
        if not sale.products:
            raise HTTPException(status_code=400, detail="La venta debe contener al menos un producto.")
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

        # insert sale details and validate products
        if not sale.products:
            raise HTTPException(status_code=400, detail="La venta debe contener al menos un producto.")
        for product in sale.products:
            # search for the product in the database
            if not product.id_product or product.stock <= 0:
                raise HTTPException(status_code=400, detail=f"Producto ID {product.id_product} no válido o cantidad insuficiente.")
            db_product = db.query(Product).filter(Product.id_product == product.id_product).first()

            if not db_product:
                raise HTTPException(status_code=404, detail=f"Producto ID {product.id_product} no encontrado.")

            # Verify if the stock is sufficient
            if db_product.stock < product.stock:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto ID {product.id_product}.")

            # calaculate subtotal and unit price
            if db_product.price is None:
                raise HTTPException(status_code=400, detail=f"El producto ID {product.id_product} no tiene un precio definido.")
            unit_price = db_product.price
            subtotal = unit_price * product.stock

            # create sale detail record
            sale_detail = SaleDetail(
                sale_id=db_sale.id,
                product_id=product.id_product,
                quantity=product.stock,
                unit_price=unit_price,
                subtotal=subtotal
            )
            db.add(sale_detail)

            # Actualizar stock del producto
            db_product.stock -= product.stock

        db.commit()

        return SaleRegisterSuccess(
            message="Venta registrada exitosamente",
            id_sale=db_sale.id
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")

# Get all sales
def get_all_sales(db: Session):
    try:
        sales = db.query(Sale).all()
        return sales
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")