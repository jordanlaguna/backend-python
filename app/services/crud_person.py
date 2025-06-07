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

    # Return useful info
    return {
        "message": "Registro exitoso",
        "id_user": db_user.id_user,
        "id_person": db_person.id_person
    }

# get person and user information
def get_allpersons_information(db: Session):
    return (
        db.query(Person, User)
        .join(User, Person.id_person == User.id_user)
        .all()
        )