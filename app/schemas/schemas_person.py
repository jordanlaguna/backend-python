from pydantic import BaseModel

class PersonRegister(BaseModel):
    # Person attributes
    birth_date: str
    identification: int
    name: str
    lastName: str
    secondName: str
    telephone: int

    # User attributes
    email: str
    password: str

class PersonUserInformation(BaseModel):
    id_person: int
    birth_date: str
    identification: int
    name: str
    lastName: str
    secondName: str
    telephone: int
    id_user: int
    email: str
    
    model_config = {
        "from_attributes": True
    }

class PersonResponse(BaseModel):
    id_person: int
    birth_date: str
    identification: int
    name: str
    lastName: str
    secondName: str
    telephone: int
    email: str

    model_config = {
        "from_attributes": True
    }

class PersonRegisterSuccess(BaseModel):
    message: str
    id_user: int
    id_person: int
