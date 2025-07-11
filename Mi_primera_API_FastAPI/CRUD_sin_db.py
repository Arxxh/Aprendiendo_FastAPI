"""
entender los endpoints CRUD (Create, Read, Update, Delete)
"""
from fastapi import FastAPI # instancia de app (iniciamos framework)
from pydantic import BaseModel # heredacion para los modelos y que se puede serializar, validacion y parsing
from typing import Optional # metodo sugerido por fastapi y pydantic en las nuevas versions para tipos de datos opcionales o ambos datos
from fastapi import status # codigos de status en http
from fastapi import HTTPException # codigos de error o excepciones si falla o no se encuentra. manejo de errores

# aqui hacemos la instancia del framework "app"
app = FastAPI(summary="Endpoints CRUD", docs_url="/docs",
              title="Rutas CRUD", version="0.0.3",description="usos de rutas con modelos aplicado CRUD")

"""
Create-POST:
Crear o subir al servidor algun dato por el protocolo HTTP o HTTPS

Read-GET:
leer algun dato creado

Update-PUT:
actualizar un dato, nombre o cualquier atributo

Delete-DELETE:
borrar un objeto serializado 
"""
# simulacion de db (lista vacia)
tasks_db:list[dict] = []
next_task_id = 1 # var para llevar la contabilidad de los id en una lista

# creamos objeto Task
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# modelo a tomar para que fastapi sepa que tipo de modelo es borrable
class DeleteResponse(BaseModel):
    mensaje:str
    task: Task


@app.post("/tasks", 
          summary="Crear nueva tarea",response_model=Task,
          response_description="Modelo tarea",status_code=status.HTTP_201_CREATED) # convencion REST 
async def create_task(task:Task) -> Task:
    global next_task_id
    # contador de id sintetico para la ruta de una db simulada
    task_dict = task.model_dump() # conversion del modelo a diccionario
    task_dict["id"] = next_task_id # Asignar el ID antes de añadirlo a la base de datos simulada
    tasks_db.append(task_dict) # ponerlo al final es decir a la cola
    next_task_id += 1 # por cada ejecucion aumenta el contador.
    return task_dict
"""a lo que entendi esta ruta "create task" creamos un id para cada task y lo ponemos al final cada ves que creamos uno con .append"""


# ver lista de tareas
@app.get("/task", summary="Ver lista de tareas")
async def list_task():
    return tasks_db



# obtener una tarea por ID
@app.get("/task/{task_id}", summary="Obtener una tarea por ID", response_model=Task)
async def get_task(task_id: int):
    for task_item in tasks_db: # recordemos que es un diccionario esto por eso esta estructura
        if task_item["id"] == task_id:
            return task_item
    raise HTTPException(status_code=404, detail="Tarea no encontrada")



# actualizar tarea por id
@app.put("/task/{task_id}", summary="actualizar tarea",response_model=Task)
async def update_task(task_id:int, updated_task:Task):
    for task_item in tasks_db:
        if task_item["id"] == task_id:
            # Actualizar los campos del diccionario existente
            task_item["title"] = updated_task.title
            task_item["description"] = updated_task.description
            task_item["completed"] = updated_task.completed
            # No actualizamos el ID aquí, ya que debe ser inmutable
            return task_item
    raise HTTPException(status_code=404, detail="Tarea no encotrada")



# borrar tarea por id
@app.delete("/task/{task_id}", summary="Borrar tarea por ID", response_model=DeleteResponse)
async def delete_task(task_id: int):
    for idx, task_item in enumerate(tasks_db):
        if task_item["id"] == task_id:
            deleted = tasks_db.pop(idx)
            return {"mensaje":"Tarea eliminada", "task":Task(**deleted)}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
