from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_clients import ClientRegister, ClientUserInformation, ClientRegisterSuccess
from app.services import crud_client
from app.models.model_client import Client
router = APIRouter()

# Obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new client
@router.post("/register_client", response_model=ClientRegisterSuccess)
def register_client(client: ClientRegister, db: Session = Depends(get_db)):
    existing_client = db.query(Client).filter(Client.identification == client.identification).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con esta identificación.")
    
    return crud_client.create_client(db=db, client=client)


# Get information of all clients
@router.get("/clients_list", response_model=list[ClientUserInformation])
def get_clients_list(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients
