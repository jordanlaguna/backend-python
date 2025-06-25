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
def get_product_by_barcode(db: Session, barcode: str) -> Product | None:
    return db.query(Product).filter(Product.barcode == barcode).first()
