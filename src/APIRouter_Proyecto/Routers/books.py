from fastapi import APIRouter, status, HTTPException, Depends
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

@router.get("/", summary="mostrar libros", ) # agregando dependencia
async def ver_libros():
    return {"mensaje":"Acceso autorizado, datos protegidos"}, books_db

@router.get("/{libro_id}", summary="ver libro por id", response_model=Book)
async def libro_por_id(libro_id:int):
    for libro_item in books_db:
        if libro_item["id"] == libro_id:
            return libro_item
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@router.put("/{libro_id}", summary="actualizar libro", response_model=Book)
async def update_book(libro_id:int, updated_book: Book):
    for book_item in books_db:
        if book_item["id"] == libro_id:
            book_item["title"] = updated_book.title
            book_item["author"] = updated_book.author
            book_item["year"] = updated_book.year
            book_item["available"] = updated_book.available
            return book_item
    raise HTTPException(status_code=404, detail="libro no encontrado")

@router.delete("/{libro_id}", summary="borrar libro", response_model=DeleteResponse)
async def delete_book(libro_id:int):
    for idx, book_item in enumerate(books_db):
        if book_item["id"] == libro_id:
            deleted = books_db.pop(idx)
            return {"mensaje": "Libro eliminado", "book": Book(**deleted)}
    raise HTTPException(status_code=404, detail="libro no encontrado")


