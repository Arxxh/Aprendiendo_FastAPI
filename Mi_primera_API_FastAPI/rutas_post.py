"""
-FastAPI utiliza Pydantic y se complementa con el framework junto con Starlette
-Pydantic es la biblioteca de validación de datos más utilizada para Python

uno de los usos mas comunes en FastAPI de la biblioteca Pydantic es la serializacion de datos
que es la conversion de objetos en python (con instancias pydantic) en JSON para el envio de
datos por servidor

esto lo aplicaremos aqui. al igual que parsin y validacion
"""

from fastapi import FastAPI
from pydantic import BaseModel 
from pydantic import field_validator # validador
from typing import Optional # esto para colocar datos opcionales en el objeto o modelo
from typing import Union # o podemos hacerlo de esta otra manera con Union 2 tipos de datos 



app = FastAPI(description="usos de rutas con modelos", title="Aprendiendo_FastAPI",
              summary="practicando y trabajando FastAPI", version="0.0.2", docs_url="/docs")

# Definimos un modelo de datos usando Pydantic

"""
objeto Item compuesto por nombre,descripcion,precio,impuestos
clase Item con 4 atributos pasandole BaseModel para que pydantic reconozca el modelo
"""
# Definimos un modelo de datos usando Pydantic y validamos que precio no tiene que ser 0
class Item(BaseModel):
    name: str
    description: Optional[str] = None # Opcional
    price: float 
    tax: Union[float, None] = None # asi tambien podemos hacerlo
    quantity: int
    
    # Validador: price debe ser mayor a 0
    @field_validator('price')
    def price_must_be_positive(cls, v): # cls es class, v es el valor a validar
        if v < 0:
            raise ValueError('El precio debe ser mayor o igual a 0')
        return v


# hacemos un endpoint para poder "enviar" este objeto para eso usamos POST
# solo se puede hacer en /docs
@app.post("/items/", summary="Crear un item", description="Recibe datos de un item y los devuelve como confirmación")
async def crear_item(item:Item): # referenciamos el objeto guardada en una variable
    return {"Mensaje":"Item recibido correctamente", "item":item}

@app.post("/items/discounted/", summary="Item con descuento", description="item + porcentaje de descuento y devuelve el precio final.")
async def item_discount(item:Item, descuento:float):
    precio_final = item.price * (1-descuento/100) # 1 para aplicarlo en porcentaje
    return {
        "Item":item,
        "descuento_aplicado": descuento,
        "precio_final": round(precio_final, 2) # redondea un numero flotante
    } # se le pasa preciofinal y el numero a redondear 2 cifras
