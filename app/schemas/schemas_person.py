from pydantic import BaseModel

class PersonRegister(BaseModel):
    # Person attributes
    birth_date: str
    identification: str
    name: str
    lastName: str
    secondName: str
    telephone: str

    # User attributes
    email: str
    password: str

class PersonUserInformation(BaseModel):
    id_person: int
    birth_date: str
    identification: str
    name: str
    lastName: str
    secondName: str
    telephone: str
    id_user: int
    email: str
    
    model_config = {
        "from_attributes": True
    }

class UpdatePerson(BaseModel):
    birth_date: str | None = None
    identification: str | None = None
    name: str | None = None
    lastName: str | None = None
    secondName: str | None = None
    telephone: str | None = None
    email: str | None = None
class PersonResponse(BaseModel):
    id_person: int
    birth_date: str
    identification: str
    name: str
    lastName: str
    secondName: str
    telephone: str
    email: str

    model_config = {
        "from_attributes": True
    }

class UpdatePersonResponse(BaseModel):
    message: str
    id_person: int

class PersonRegisterSuccess(BaseModel):
    message: str
    id_user: int
    id_person: int
