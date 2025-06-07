from fastapi import FastAPI
from app.database.database import Base, engine
from app.router import user_routes
from app.router import person_routes
from app.models.model_person import Person

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Postsys API")

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(person_routes.router, prefix="/persons", tags=["Persons"])
@app.get("/")
def root():
    return {"message": "API de reservas activa 🚀"}
