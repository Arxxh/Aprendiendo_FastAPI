from pydantic import BaseModel

# modelo de solicitud de inicio de sesión
class Login_Request(BaseModel):
    username: str
    password: str

# modelo token 
class Token(BaseModel):
    access_token: str
    token_type: str

# registrar usuario
class RegisterUser(BaseModel):
    username: str
    password: str