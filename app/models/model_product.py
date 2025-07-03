from app.database.database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric


class Product(Base):
    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    barcode = Column(String(100), nullable=True)
    created_at = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  
