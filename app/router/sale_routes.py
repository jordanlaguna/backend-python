import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.model_product import Product
from app.models.model_sale_details import SaleDetail
from app.schemas.schemas_sales import SaleRegister, SaleRegisterSuccess, SalesList
from app.services import crud_sale
from app.models.model_sales import Sale
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
import tempfile

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

# Get all sales
@router.get("/sales_list", response_model=List[SalesList])
def get_all_sales(db: Session = Depends(get_db)):
    sales = crud_sale.get_all_sales(db=db)
    return sales

# generate a sale report
@router.get("/pdf/{sale_id}", response_class=FileResponse)
def generate_invoice_pdf(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    # obtain sale details
    if not sale.details:
        raise HTTPException(status_code=404, detail="Detalles de la venta no encontrados")
    details = db.query(SaleDetail).filter(SaleDetail.sale_id == sale.id).all()

    # Create PDF file in temporary directory
    temp_dir = Path(os.getenv("TEMP") or Path(tempfile.gettempdir()))
    file_path = temp_dir / f"venta_{sale.sale_number}.pdf"

    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"Factura: {sale.sale_number}")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Fecha: {sale.created_at.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    c.drawString(50, y, f"Método de pago: {sale.payment_method}")
    y -= 20
    c.drawString(50, y, f"Total: ₡{sale.total:,.2f}")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Detalles:")
    y -= 20

    c.setFont("Helvetica", 12)
    for detail in details:
        product = db.query(Product).filter(Product.id_product == detail.product_id).first()
        if product:
            c.drawString(50, y, f"{product.name} - Cantidad: {detail.quantity} - Precio: ₡{detail.unit_price:,.2f} - Subtotal: ₡{detail.subtotal:,.2f}")
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50

    c.save()

    return FileResponse(path=file_path, filename=file_path.name, media_type='application/pdf')