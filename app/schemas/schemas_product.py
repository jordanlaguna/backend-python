from pydantic import BaseModel
import datetime

class ProductRegister(BaseModel):
    # Product attributes
    name: str
    description: str
    price: float
    stock: int
    barcode: str
    created_at: datetime.datetime
    category_id: int

class ProductResponse(BaseModel):
    id_product: int
    name: str
    description: str
    price: float
    stock: int
    barcode: str
    created_at: datetime.datetime
    category_id: int

    model_config = {
        "from_attributes": True
    }

class ProdcutRegisterSuccess(BaseModel):
    message: str
    id_product: int

    model_config = {
        "from_attributes": True
    }