from sqlalchemy.orm import Session
from app.models.model_product import Product
from app.models.model_categories import Category
from app.schemas.schemas_product import ProductRegister, ProductResponse, ProdcutRegisterSuccess

def create_product(db: Session, product: ProductRegister):
    # Create a new product
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        barcode=product.barcode,
        category_id=product.category_id,
        created_at=product.created_at,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Return useful info
    return ProdcutRegisterSuccess(
        message="Producto registrado exitosamente",
        id_product=db_product.id_product
    )

def get_all_products(db: Session):
    # Get all products with their categories
    return (
        db.query(Product, Category)
        .join(Category, Product.category_id == Category.id)
        .all()
    )

# Get a product by barcode
def get_product_by_barcode(db: Session, name: str) -> Product | None:
    return db.query(Product).filter(Product.name == name).first()

# Update product information
def update_product_information(db: Session, id_product: int, product_data: dict):
    db_product = db.query(Product).filter(Product.id_product == id_product).first()
    if not db_product:
        return None
    for  key, value in product_data.items():
        if value is not None:
            # Update fields in Product
            if hasattr(db_product, key):
                setattr(db_product, key, value)
            else:
                raise ValueError(f"Unknown field: {key}")
    db.commit()
    db.refresh(db_product)
    return {
        "message": "Información del producto actualizada exitosamente",
        "id_product": db_product.id_product
    }