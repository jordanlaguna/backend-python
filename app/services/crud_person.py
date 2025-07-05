from sqlalchemy.orm import Session
from app.models.model_person import Person
from app.models.model_user import User
from app.schemas.schemas_person import PersonRegister
from app.utils.security import hash_password

def create_person(db: Session, person: PersonRegister):
    # Create a new person
    db_person = Person(
        birth_date=person.birth_date,
        identification=person.identification,
        name=person.name,
        lastName=person.lastName,
        secondName=person.secondName,
        telephone=person.telephone
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

    # Create a new associated user
    db_user = User(
        email=person.email,
        password=hash_password(person.password),
        id_person=db_person.id_person
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "Registro exitoso",
        "id_user": db_user.id_user,
        "id_person": db_person.id_person
    }

# Get all persons and their user info
def get_allpersons_information(db: Session):
    return (
        db.query(Person, User)
        .join(User, Person.id_person == User.id_person)
        .all()
    )

# Update person and user information
def update_person_information(db: Session, id_person: int, person_data: dict):
    db_person = db.query(Person).filter(Person.id_person == id_person).first()
    db_user = db.query(User).filter(User.id_person == id_person).first()

    if not db_person or not db_user:
        return None

    for key, value in person_data.items():
        if value is not None:
            # Update fields in Person
            if hasattr(db_person, key):
                setattr(db_person, key, value)
            # Update email
            elif key == "email":
                db_user.email = value
            else:
                raise ValueError(f"Campo desconocido: {key}")

    db.commit()
    db.refresh(db_person)

    return {
        "message": "Persona actualizada exitosamente",
        "id_person": id_person
    }
