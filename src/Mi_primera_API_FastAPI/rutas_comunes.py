"""
importamos la app y creamos una instancia
"""
from fastapi import FastAPI

app = FastAPI(title="Aprendiendo_FastAPI",summary="Practicando y trabajando FastAPI",
              description="Mi primera ruta", version="0.0.1", docs_url="/docs")

"""
ruta normal, solo devolviendo un diccionario ruta:holamundo
"""
@app.get("/primera_ruta")
async def mi_primera_ruta():
    return {"Mi primera ruta":"Hola Mundo"}

"""
en el buscador del servidor le pasamos un {nombre} que queramos. la funcion lo procesa y 
te entrega un mensaje con el nombre que le pasaste
"""
# Ruta practica devolviendo un saludo
@app.get("/saludo/{nombre}", summary="saludar por nombre", description="devuelve un saludo")
async def saludar(nombre:str):
    return {"mensaje":f"Hola {nombre}"}

"""
en el buscador del servidor le pasamos un dato entero (1,23,56 o el que sea) y la funcion
va a procesar un interador en una list comprehension. diciendo regresame el iterador
en forma de un diccionario ""items{i}"" y creamos el contador diciendo que empiece a contar 
en el rango de 1 al numero del limite +1 dado que range() no contempla el valor ultimo es decir
si es 53 te regresa sin el +1 te regresa 52
"""
#ruta con queryparam limit mas 1 por que range no toma en cuenta el valor final
@app.get("/items/", summary="Listar Items", description="Devuelve una lista limitada de items")
async def lista_items(limit: int = 10):
    return {"items": [f"Item {i}" for i in range(1, limit+1)]} # List Comprehension

"""
ruta sin mas solo para comunicacion similar a mi primera ruta
"""
# Ruta GET sin parámetros Similar a "primera_ruta"
@app.get("/ping", summary="Ping simple", description="Endpoint para probar que el servidor funciona")
async def ping():
    return {"status":"ok"}

#ruta con 2 parametros
"""
Al url le pasamos 2 parametros para lograr la suma. la funcion asincrona lo procesa y retorna 
el resultado de la suma
"""
@app.get("/suma/{a}/{b}", summary="Suma de dos numeros", description="Recibe dos números en la URL y devuelve su suma")
async def suma(a: int, b: int):
    return {"resultado": a + b}

@app.get("/multiplicacion/{a}/{b}", summary="Suma de dos numeros", description="Recibe dos números en la URL y devuelve su suma")
async def multiplicacion(a: int, b: int):
    return {"resultado": a * b}

@app.get("/multiplicacion_no_entera/{a}/{b}", summary="Suma de dos numeros", description="Recibe dos números en la URL y devuelve su suma")
async def multiplicacion_flotante(a: float, b: float):
    return {"resultado": a * b}
"""
devuelve un mensaje en json por defecto pero a la url tenemos que pasarle "?" que normalmente 
en algunos frameworks de front se manejan para decir que un campo no es obligatorio
"""
# Ruta con parámetro de consulta opcional ?texto="texto.."
@app.get("/mensaje/",summary="Un mensaje opcional", description="Devuelve un mensaje o uno por defecto si no se envía")
async def mensaje(texto:str = "Hola mundo por defecto"):
    return {"mensaje":texto}

