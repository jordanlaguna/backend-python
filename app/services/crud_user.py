from sqlalchemy.orm import Session
from app.models.model_user import User
from app.schemas.schemas_user import UserCreate, UserUpdate
from app.utils.security import hash_password, verify_password 

# get all users 
def get_users(db: Session):
    return db.query(User).all()

# get a user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id_user == user_id).first()

# create a new user
def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = User(
        email=user.email,
        password=hashed,
        id_person=user.id_person
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# authenticate user (para login)
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user