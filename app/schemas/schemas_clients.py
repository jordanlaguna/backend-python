from pydantic import BaseModel
from datetime import date


class ClientRegister(BaseModel):
    # client attributes
    identification: str
    name: str
    last_name: str
    second_name: str
    email: str
    telephone: int | None = None
    address: str | None = None
    register_date: str | None = None

class ClientResponse(BaseModel):
    id_client: int
    identification: str
    name: str
    last_name: str
    second_name: str
    email: str
    telephone: int | None = None
    address: str | None = None
    register_date: str | None = None

    model_config = {
        "from_attributes": True
    }

class ClientRegisterSuccess(BaseModel):
    message: str
    id_client: int

    model_config = {
        "from_attributes": True
    }
class ClientUserInformation(BaseModel):
    id_client: int
    identification: str
    name: str
    last_name: str
    second_name: str
    email: str
    telephone: int | None = None
    address: str | None = None
    register_date: date | None = None

    model_config = {
        "from_attributes": True
    }