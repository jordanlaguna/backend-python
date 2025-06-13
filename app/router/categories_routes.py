from app.models.model_categories import Category
from app.schemas.schemas_categories import CategoryRegister, CategoryResponse, AddCategories
from app.services.crud_categories import create_category, get_all_categories
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal

roueter = APIRouter()

# Create to connect to the database

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new category
@roueter.post("/register_category", response_model=AddCategories)
def register_category(category: CategoryRegister, db: Session = Depends(get_db_session)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Categoría ya registrada con este nombre.")
    return create_category(db=db, category=category)

# Get a list of all categories 
@roueter.get("/categories_list", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db_session)):
    return get_all_categories(db=db)