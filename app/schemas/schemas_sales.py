from pydantic import BaseModel
import datetime
from decimal import Decimal

class ProductSale(BaseModel):
    id_product: int
    stock: int


class SaleRegister(BaseModel):
    sale_number: str
    client_id: int  
    user_id: int
    total: Decimal
    subtotal: Decimal
    tax: Decimal    
    payment_method: str
    cash_received: Decimal
    change_given: Decimal
    created_at: datetime.datetime
    products: list[ProductSale]

class SaleResponse(BaseModel):
    id_sale: int
    sale_number: str
    client_id: int  
    user_id: int
    total: Decimal
    subtotal: Decimal
    tax: Decimal
    payment_method: str
    cash_received: Decimal
    change_given: Decimal
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }
class SaleRegisterSuccess(BaseModel):
    message: str
    id_sale: int

    model_config = {
        "from_attributes": True
    }