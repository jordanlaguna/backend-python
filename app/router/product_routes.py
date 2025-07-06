from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_product import ProductRegister, ProductResponse, ProdcutRegisterSuccess, ProductUpdate, ProductUpdateResponse
from app.services import crud_product
from app.models.model_product import Product

router = APIRouter()

# Obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new product
@router.post("/add_product", response_model = ProdcutRegisterSuccess)
def register_product(product: ProductRegister, db: Session = Depends(get_db)):

    existing_product = db.query(Product).filter(Product.barcode == product.barcode).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Ya existe un producto con este código de barras.")

    # Register the product + category
    return crud_product.create_product(db=db, product=product)

# Get all products
@router.get("/products_list", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    # Get all products with their categories
    products = crud_product.get_all_products(db=db)

    # Convert the results to a list of ProductResponse
    result = []
    for product, category in products:
        result.append(
            ProductResponse(
                id_product=product.id_product,
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                barcode=product.barcode,
                created_at=product.created_at,
                category_id=product.category_id,
            )
        )
    
    return result

# Get a product by name
@router.get("/product/{name}", response_model=ProductResponse)
def get_product_by_barcode(name: str, db: Session = Depends(get_db)):
    product = crud_product.get_product_by_barcode(db=db, name=name)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product
# Search products by name dynamically
@router.get("/search/{name}", response_model=List[ProductResponse])
def search_products_by_name(name: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
    return products

# Update product information
@router.put("/update_product/{id_product}", response_model=ProductUpdateResponse)
def update_product(id_product: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id_product == id_product).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    updated_product = crud_product.update_product_information(
        db=db,
        id_product=id_product,
        product_data=product_data.dict()
    )

    if not updated_product:
        raise HTTPException(status_code=400, detail="Error al actualizar la información del producto.")
    
    return updated_product