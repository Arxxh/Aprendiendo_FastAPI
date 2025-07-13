from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException, status, APIRouter


# creamos una agrupacion de rutas /tasks
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]

)


# simulacion de db (lista vacia)
tasks_db:list[dict] = []
next_task_id = 1 # var para llevar la contabilidad de los id en una lista

# creamos objeto Task
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# regrese un modelo response_model = "DeleteResponse"
class DeleteResponse(BaseModel):
    mensaje: str
    task: Task

# dado a que es una agrupacion se llama router en ves de app
@router.post("/crear_tarea", 
          summary="Crear nueva tarea",response_model=Task,
          response_description="Modelo tarea",
          status_code=status.HTTP_201_CREATED) # convencion REST 
async def create_task(task:Task) -> Task:
    global next_task_id
    # contador de id sintetico para la ruta de una db simulada
    task_dict = task.model_dump() # conversion del modelo a diccionario
    task_dict["id"] = next_task_id # Asignar el ID antes de añadirlo a la base de datos simulada
    tasks_db.append(task_dict) # ponerlo al final es decir a la cola
    next_task_id += 1 # por cada ejecucion aumenta el contador.
    return task_dict

@router.get("/lista", summary="ver lista de tareas", response_model=list[Task])
async def ver_list():
    return tasks_db

@router.get("/{task_id}", summary="ver lista por id")
async def lista_by_id(task_id: int):
    for task_item in tasks_db:
        if task_item["id"] == task_id:
            return task_item
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.put("/actualizar/{task_id}", response_model=Task)
async def actualizar_lista(task_id:int, updated_task:Task):
    for idx, task_item in task_item:
        if task_item["id"] == task_id:
            task_item["title"] = updated_task.title
            task_item["description"] = updated_task.description
            task_item["completed"] = updated_task.completed
            # no actualizar id por que es inmutable
            return task_item
            # Actualizar los campos del diccionario existente
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@router.delete("/borrar/{task_id}", response_model=DeleteResponse)
async def borrar_tarea(task_id:int):
    for idx, task_item in enumerate(tasks_db):
        if task_item["id"] == task_id:
            deleted = tasks_db.pop(idx)
            return {"mensaje":"Tarea borrada", "task":Task(**deleted)}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

