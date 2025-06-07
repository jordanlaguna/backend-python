from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_user import Login, UserCreate, UserUpdate, UserResponse
from app.services import crud_user
from app.utils.security import verify_password

router = APIRouter()

# get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# List all users
@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

#Login
@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    user_found = crud_user.authenticate_user(db, user.email, user.password)
    if not user_found:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Login exitoso", "user_id": user_found.id_user}

# Get a user by ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# Create a new user
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)
