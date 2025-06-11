from sqlalchemy.orm import Session
from app.models.model_client import Client
from app.schemas.schemas_clients import ClientRegister

def create_client(db: Session, client: ClientRegister):
    # Create a new client instance
    db_client = Client(
        identification=client.identification,
        name=client.name,
        last_name=client.last_name,
        second_name=client.second_name,
        email=client.email,
        telephone=client.telephone,
        address=client.address,
        register_date=client.register_date
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return {
        "message": "Client registered successfully",
        "id_client": db_client.id_client
    }

def get_all_clients_information(db: Session):
    # Retrieve all clients from the database
    return db.query(Client).all()
