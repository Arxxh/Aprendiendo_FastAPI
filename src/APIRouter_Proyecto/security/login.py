# auth.py

from fastapi import APIRouter, HTTPException
from security.schemas.schemas_auth import Token, Login_Request
from datetime import datetime, timedelta, timezone
from jose import jwt
from security.db_simulada.db import fake_users_db, pwd_context

router = APIRouter(prefix="/auth",
                   tags=["auth"])
 
# SECRET_KEY para firmar el JWT
SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=Token)
def login(login_data: Login_Request):
    # Busca al usuario en la lista simulada
    user = next((u for u in fake_users_db if u["username"] == login_data.username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verifica la contraseña
    if not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Crea el token de acceso
    access_token = create_access_token(
        data={"sub": user["username"], "id": user["id"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}