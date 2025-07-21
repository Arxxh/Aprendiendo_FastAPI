
from fastapi import APIRouter, HTTPException, status, Depends
from security.schemas.schemas_auth import RegisterUser
from security.db_simulada.db import fake_users_db, next_user_id, pwd_context


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    global next_user_id  # Para modificar la variable global

    # Verifica si el usuario ya existe
    for u in fake_users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Usuario ya registrado")
    
    # Hashea la contraseña del usuario
    hashed_password = pwd_context.hash(user.password)
    
    # Crea un nuevo usuario con un ID único
    new_user = {
        "id": next_user_id,
        "username": user.username,
        "hashed_password": hashed_password,
    }
    fake_users_db.append(new_user)  # Agrega el nuevo usuario a la base de datos simulada
    next_user_id += 1  # Incrementa el ID para el próximo usuario

    return {"msg": f"Usuario '{user.username}' registrado exitosamente"}
