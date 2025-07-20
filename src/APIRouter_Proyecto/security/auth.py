"""
Simulacion de la autenticacin de un token (Header)
"""

from fastapi import HTTPException, Header, status, Depends

# simulacion de un token de autenticacion
API_KEY = "secreto123"

"""
x_token de usuario es la entrada para que header lo entienda a su propio X-token Serializacion
"""
def verificar_token(x_token:str = Header(...)): # conversion
    if x_token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Inválido"
        )
    return True

