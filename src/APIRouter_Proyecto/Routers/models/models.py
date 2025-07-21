from pydantic import BaseModel
from typing import Optional



"""
modelos de archivo books
"""
class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int
    available: Optional[bool] = True # por que true y no None si no lo sabemos?

class DeleteResponse(BaseModel):
    mensaje: str
    book: Book


"""
modelos de archivo users
"""
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: Optional[int] = None

class DeleteResponse(BaseModel):
    mensaje : str
    usuario : User


"""
modelos de archivo tasks
"""
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

class DeleteResponse(BaseModel):
    mensaje: str
    task: Task
