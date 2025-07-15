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
@router.post("/", summary="crear un libro",
              response_model=Book, status_code=status.HTTP_201_CREATED)
async def crear_libro(book:Book):
    global next_id_books
    book_dict = book.model_dump()
    book_dict["id"] = next_id_books
    books_db.append(book_dict)
    next_id_books += 1
    return book_dict

@router.get("/", summary="mostrar libros")
async def ver_libros():
    return books_db

@router.get("/{libro_id}", summary="ver libro por id", response_model=Book)
async def libro_por_id(libro_id:int):
    for libro_item in books_db:
        if libro_item["id"] == libro_id:
            return libro_item
    raise HTTPException(status_code=404, detail="Libro no encontrado")


