from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#contraseña mongodb 6SuyxJ0SbQ2ahcuD
#user abreuh519

# Configuración
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 15  # Aumentamos la duración para pruebas (15 minutos)
SECRET = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYXJvbGQiLCJuYW1lIjoiSGFyb2xkIEFicmV1IiwiZXhwIjoxNTE2MjM5MDIyfQ.TCPdc8In-SRDrSMSdcn9NnCR9XuzBr8mZu7idYC8inI"

router = APIRouter(tags=["autenticacion"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

# Modelo de usuario
class User(BaseModel):
    full_name: str
    user_name: str
    email: str
    disabled: bool

class UserDb(User):
    password: str

# Base de datos simulada 
users_db = {
    "harold": {
        "full_name": "Harold Abreu",
        "user_name": "harold", 
        "email": "harold@abreu.com",
        "disabled": False,
        "password": "$2a$12$q76PhsuBuValZGPbWL40WOAYL/tHQlhznkU3uKGZ2BNE6sQCtyToW"
    },
    "antonio": {
        "full_name": "Antonio Rick",
        "user_name": "antonio",  
        "email": "ant@antoniodev.com",
        "disabled": False,
        "password": "$2a$12$wyhR.FSgexvf1269kjul2ewKbSB6BdlAqyHlgcoA9TKef4jUbFYjC"
    }
}

def search_user_db(user_name: str):
    if user_name in users_db:
        return UserDb(**users_db[user_name])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Función para obtener el usuario actual
async def auth_user(token: str = Depends(oauth2)):
    auth_exception = HTTPException(  
        status_code=401,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise auth_exception
    except JWTError:
        raise auth_exception
    
    user = search_user(username)
    if user is None:
        raise auth_exception
    return user

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Usuario inactivo",
        ) 
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    access_token_data = {
        "sub": user.user_name,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    access_token = jwt.encode(access_token_data, SECRET, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "Bearer"}

# Ruta para obtener el perfil del usuario autenticado
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
