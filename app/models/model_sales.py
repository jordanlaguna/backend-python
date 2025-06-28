from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from app.database.database import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(100), unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id_client"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    cash_received = Column(Numeric(10, 2), nullable=False)
    change_given = Column(Numeric(10, 2), nullable=False)
    created_at = Column(Date, nullable=False)
