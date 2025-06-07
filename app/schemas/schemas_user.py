from pydantic import BaseModel

# User schemas for user management in the application
class UserCreate(BaseModel):
    email: str
    password: str
    id_person: int | None = None  
class Login(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id_user: int
    email: str
    id_person: int | None = None  

    model_config = {
        "from_attributes": True
    }