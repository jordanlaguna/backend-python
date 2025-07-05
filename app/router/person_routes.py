from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.schemas_person import PersonRegister, PersonRegisterSuccess, PersonResponse, PersonUserInformation, UpdatePersonResponse, UpdatePerson
from app.services import crud_person
from app.models.model_person import Person
from app.models.model_user import User

router = APIRouter()

# obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register complete (person + user)
@router.post("/register", response_model=PersonRegisterSuccess)
def register_person(person: PersonRegister, db: Session = Depends(get_db)):
    # Verify if the person already exists
    existing_person = db.query(Person).filter(Person.identification == person.identification).first()
    if existing_person:
        raise HTTPException(status_code=400, detail="Ya existe una persona con esta cédula.")

    # Verify if the user already exists
    existing_user = db.query(User).filter(User.email == person.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este correo.")

    # Register person + user
    return crud_person.create_person(db=db, person=person)

# get information of all persons and users
@router.get("/persons_list", response_model=List[PersonUserInformation])
def get_all_persons(db: Session = Depends(get_db)):
    # Get all persons and their associated users
    persons = (
        db.query(Person, User)
        .join(User, Person.id_person == User.id_person)
        .all()
    )

    # Convert the results to a list of PersonUserInformation
    result = []
    for person, user in persons:
        result.append(
            PersonUserInformation(
                id_person=person.id_person,
                birth_date=person.birth_date,
                identification=person.identification,
                name=person.name,
                lastName=person.lastName,
                secondName=person.secondName,
                telephone=person.telephone,
                id_user=user.id_user,
                email=user.email
            )
        )
    return result

# Update a person by ID
@router.put("/update/{id_person}", response_model=UpdatePersonResponse)
def update_person(id_person: int, person: UpdatePerson, db: Session = Depends(get_db)):

    # Verify if the person exists
    existing_person = db.query(Person).filter(Person.id_person == id_person).first()
    if not existing_person:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")

    # Update person information
    updated_person = crud_person.update_person_information(db=db, id_person=id_person, person_data=person.dict())
    if not updated_person:
        raise HTTPException(status_code=400, detail="Error al actualizar la persona.")

    return updated_person