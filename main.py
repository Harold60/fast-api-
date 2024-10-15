from fastapi import FastAPI
from routers import productos, users_db, auth_JWT

# Comando para desplegar server: python -m uvicorn main:app --reload

# instancia de la aplicación
app = FastAPI(
    title="API de Productos y Usuarios",
    description="Una API simple para gestionar productos y usuarios",
    version="1.0.0",
    contact={
        "name": "Tu Harold",
        "email": "harold@gmail.com",
    },
)

# routers de otros módulos
app.include_router(productos.router)
app.include_router(users_db.router)

# app.include_router(basic_auth.router)
app.include_router(auth_JWT.router)

# Ruta raíz con mensaje de bienvenida
@app.get("/", tags=["Main"])
async def root():
    """
    Ruta principal con un mensaje de bienvenida.
    """
    return {"mensaje": "¡Bienvenido a la API!"}

