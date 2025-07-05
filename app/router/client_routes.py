from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_clients import ClientRegister, ClientUserInformation, ClientRegisterSuccess, ClientUpdate,UpdateClientResponse
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

# Update client information
@router.put("/update_client/{id_client}", response_model=UpdateClientResponse)
def update_client(id_client: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    existing_client = db.query(Client).filter(Client.id_client == id_client).first()
    if not existing_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    
    updated_client = crud_client.update_client_information(
        db=db,
        id_client=id_client,
        client_data=client_data.dict()
    )

    if not updated_client:
        raise HTTPException(status_code=400, detail="Error al actualizar la información del cliente.")
    
    return updated_client

