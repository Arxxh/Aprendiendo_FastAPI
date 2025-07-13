from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# simulacion de db (lista vacia)
user_db:list[dict] = []
next_user_id = 1 # var para llevar la contabilidad de los id en una lista

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: Optional[int] = None


# regrese un modelo response_model = "DeleteResponse"
class DeleteResponse(BaseModel):
    mensaje : str
    usuario : User

@router.post("/crear_usuario", summary="Crear un usuario", response_model=User, 
            response_description="Modelo User",
            status_code=(status.HTTP_201_CREATED))
async def crear_usuario(user: User):
    global next_user_id
    user_dict = user.model_dump()
    user_dict["id"] = next_user_id
    user_db.append(user_dict)
    next_user_id += 1
    return user_dict


@router.get("/lista", summary="ver lista de usuario", response_model=list[dict])
async def ver_usuario():
    return user_db


@router.get("/lista/{user_id}", summary="ver usuario por id", response_model=User,
            response_description="modelo usuario")
async def usuario_por_id(user_id:int):
    for user_item in user_db:
        if user_item["id"] == user_id:
            return user_item
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
