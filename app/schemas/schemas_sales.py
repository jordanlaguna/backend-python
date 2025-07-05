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
    total: float
    subtotal: float
    tax: float
    payment_method: str
    cash_received: float
    change_given: float
    created_at: datetime.datetime
    products: list[ProductSale]

class SalesList(BaseModel):
    id: int
    sale_number: str
    client_id: int  
    user_id: int
    total: float
    subtotal: float
    tax: float
    payment_method: str
    cash_received: float
    change_given: float
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }
class SaleResponse(BaseModel):
    id_sale: int
    sale_number: str
    client_id: int  
    user_id: int
    total: float
    subtotal: float
    tax: float
    payment_method: str
    cash_received: float
    change_given: float
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