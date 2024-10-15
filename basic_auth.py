
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
cryp = CryptContext(schemes=["bcrypt"])


router = APIRouter(tags=["autenticacion"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Modelo de usuario
class User(BaseModel):
    full_name: str
    user_name: str
    email: str
    disabled: bool

class UserDb(User):
    password: str

# Base de datos simulada corregida
users_db = {
    "harold": {
        "full_name": "Harold Abreu",
        "user_name": "harold",  # Corregido a "harold" en minúscula
        "email": "harold@abreu.com",
        "disabled": True,
        "password": "$2a$12$q76PhsuBuValZGPbWL40WOAYL/tHQlhznkU3uKGZ2BNE6sQCtyToW"
    },
    "antonio": {
        "full_name": "Antonio Rick",
        "user_name": "antonio",  # Corregido a "antonio"
        "email": "ant@antoniodev.com",
        "disabled": False,
        "password": "$2a$12$wyhR.FSgexvf1269kjul2ewKbSB6BdlAqyHlgcoA9TKef4jUbFYjC"
    }
}

# Función para obtener el usuario actual
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales de autenticación inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Usuario inactivo",
        ) 

    return user

# Función para buscar un usuario en la base de datos
def search_user(username: str):
    user_data = users_db.get(username)
    if user_data:
        return User(**user_data)
    return None

# Ruta para el login
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = search_user(form.username.lower())  # Convertir a minúscula
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    
    if form.password != user_db.password:
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user_db.user_name, "token_type": "bearer"}

# Ruta para obtener el perfil del usuario autenticado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
