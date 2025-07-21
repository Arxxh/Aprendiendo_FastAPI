# db.py
from passlib.context import CryptContext

# Simulación de base de datos
fake_users_db: list[dict] = []

# Variable para llevar la contabilidad de los IDs
next_user_id = 1

# Contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")