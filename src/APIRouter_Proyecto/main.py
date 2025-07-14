from fastapi import FastAPI
from Routers import tasks, users, books

app = FastAPI(
    title="Mi_Api_Routers",
    summary="Aprendiendo_APIRouter",
    version="0.0.4", # la fue cambiando a archivos que hacia. llevo 4 archivos 
    description="API_Modular"
)
                  
# conexion con tasks
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(books.router)
