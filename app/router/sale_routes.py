from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_sales import SaleRegister, SaleRegisterSuccess
from app.services import crud_sale
from app.models.model_sales import Sale

router = APIRouter()

# connect to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new sale
@router.post("/add_sale", response_model=SaleRegisterSuccess)
def register_sale(sale: SaleRegister, db: Session = Depends(get_db)):
    existing_sale = db.query(Sale).filter(Sale.sale_number == sale.sale_number).first()
    if existing_sale:
        raise HTTPException(status_code=400, detail="Ya existe una venta con este número de venta.")
    if sale.cash_received < sale.total:
        raise HTTPException(status_code=400, detail="El efectivo recibido no puede ser menor al total de la venta.")
    if sale.change_given < 0:
        raise HTTPException(status_code=400, detail="El cambio dado no puede ser negativo.")
    
    # Register the sale
    return crud_sale.create_sale(db=db, sale=sale)