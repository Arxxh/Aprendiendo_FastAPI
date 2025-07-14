from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

books_db: list[dict] = []
next_id_books = 1


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    year: int
    available: Optional[bool] = True # por que true y no None si no lo sabemos?

class DeleteResponse(BaseModel):
    mensaje: str
    book: Book

# crear un libro
@router.post("/", summary="crear un libro", response_model=Book, status_code=status.HTTP_201_CREATED)
async def crear_libro():
    return
