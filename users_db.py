from fastapi import APIRouter,HTTPException
from db.models.user import User
from db.client import db_client

router = APIRouter( prefix= "/usersdb",
                    tags=["users"],
                    response= {404 :{"mensaje": "usuario no encontrado"}})


# Lista inicial de usuarios
users_list = []

# Obtener todos los usuarios
@router.get("/")
async def get_users():
    return users_list

# Obtener un usuario por ID
@router.get("/{id}")
async def get_user(id: int):
    user = search_user(id)
    if user is None:
        return {"mensaje": "Usuario no encontrado"}
    return user

# Crear un nuevo usuario
@router.post("/")
async def create_user(user: User):
    # Verificar si el usuario ya existe
    # if search_user(user.id) is not None:
    #     raise HTTPException(status_code=404,detail= "El usuario ya existe")
        
    
    # # Si no existe, agregar a la lista
    # users_list.append(user)
    # return {"mensaje": "Usuario creado con éxito", "usuario": user}
    user_dict = dict(user)

    db_client.local.users.insert_one(user_dict)

    return user

# Actualizar un usuario existente
@router.put("/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            break

    if not found:
        raise HTTPException(status_code=404 ,detail="No se ha encontrado el usuario")
    
    return {"mensaje": "Usuario actualizado con éxito", "usuario": user}

@router.delete("/{id}")
async def user_delete(id:int):
     
   found = False
   for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            break

   if not found:
        raise HTTPException(status_code=404 ,detail="No se ha encontrado el usuario")
    
   return {"mensaje": "Usuario borrado con éxito"}
    

# Función auxiliar para buscar un usuario por ID
def search_user(id: int):
    # Busca el usuario por ID en la lista
    for user in users_list:
        if user.id == id:
            return user
    return None
