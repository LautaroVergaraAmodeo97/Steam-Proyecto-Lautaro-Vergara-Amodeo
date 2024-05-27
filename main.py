from fastapi import FastAPI
from typing import Optional, List

app = FastAPI()

# Supongamos que df_bdev es un DataFrame que contiene los datos necesarios

# Función userdata
def userdata(user_id: str):
    # Simulación de la función userdata utilizando df_bdev
    return {"Usuario": user_id, "Dinero gastado": "200 USD", "% de recomendación": "20%", "cantidad de items": 5}

# Función developer
def developer(desarrollador: str):
    # Simulación de la función developer utilizando df_bdev
    return [{"Año": 2023, "Cantidad de Items": 50, "Contenido Free": "27%"}, 
            {"Año": 2022, "Cantidad de Items": 45, "Contenido Free": "25%"}]

# Función recomendacion_juego
def recomendacion_juego(product_id: int):
    # Simulación de la función recomendacion_juego utilizando df_bdev
    return ["Juego 1", "Juego 2", "Juego 3", "Juego 4", "Juego 5"]

# Función recomendacion_usuario
def recomendacion_usuario(user_id: str):
    # Simulación de la función recomendacion_usuario utilizando df_bdev
    return ["Juego 1", "Juego 2", "Juego 3", "Juego 4", "Juego 5"]

# Rutas de la API

@app.get("/userdata/{user_id}")
async def get_userdata(user_id: str):
    return userdata(user_id)

@app.get("/developer/{desarrollador}")
async def get_developer(desarrollador: str):
    return developer(desarrollador)

@app.get("/recomendacion_juego/{product_id}")
async def get_recomendacion_juego(product_id: int):
    return recomendacion_juego(product_id)

@app.get("/recomendacion_usuario/{user_id}")
async def get_recomendacion_usuario(user_id: str):
    return recomendacion_usuario(user_id)



