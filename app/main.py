from fastapi import FastAPI
from app.database.database import Base, engine
from app.router import user_routes
from app.router import person_routes
from app.router import client_routes
from app.router import product_routes
from app.router import categories_routes
from app.models.model_person import Person

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Postsys API")

# Include routers
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(person_routes.router, prefix="/persons", tags=["Persons"])
app.include_router(client_routes.router, prefix="/clients", tags=["Clients"])
app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(categories_routes.roueter, prefix="/categories", tags=["Categories"])

@app.get("/")
def root():
    return {"message": "API de reservas activa 🚀"}
