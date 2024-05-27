import importlib
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
import funcion as f
importlib.reload(f)



app = FastAPI()

@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def home():
    return '''
    <html>
        <head>
            <title>EJECUCION LOCAL API STEAM SISTEMA DE RECOMENDACION ITEMS</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Eres bienvenido a esta API de Steam</h1>
            <p>INSTRUCCIONES:</p>
            <p>Escribe <span style="background-color: lightgray;">/docs</span> al final de la URL de esta página para interactuar con la API.</p>
            
            <p style="color: #ff7e00; font-size: 20px; font-weight: bold; margin-top: 40px;">Estas son las consultas que podrás realizar al interactuar con la API</p>
<ul>
    <li><strong> Devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.</strong></li>
    <li><strong>Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)</strong></li>
    <li><strong>Obtener el top 3 de juegos más recomendados por año</strong></li>
    <li><strong>Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.</strong></li>
    <li><strong>Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.</strong></li>
    <li><strong>Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora</strong></li>
    <li><strong>Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.</strong></li>
</ul>
        </body>
    </html>
    '''


@app.get('/user_for_genre',
         description=""" <font color="blue">
                    1. Haga click en aquí.<br>
                    2. Ingrese el género .<br>
                    3. Le va a mostrar los datos proporcionados.
                    </font>
                    """,
         tags=["Consultas Generales"])
def UserForGenre(genero: str = Query(..., 
                            description="Género del videojuego", 
                            example='Action')):
    return f.UserForGenre(genero)



@app.get('/best_games_year',
         description="Encuentra los juegos más recomendados para un año específico.",
         tags=["Modelo de recomendación"])
def best_games_year(year: int = Query(..., 
                                      description="Año para el que se desea encontrar los juegos más recomendados", 
                                      example=2022)):
    """
    Encuentra los juegos más recomendados para un año específico.

    Parameters:
    - year (int): Año para el que se desea encontrar los juegos más recomendados.

    Returns:
    - dict: Información sobre los juegos más recomendados.
    """
    return f.best_games_year(year)


@app.get('/developer_reviews_analysis',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga click en "Quiero probar".<br>
                    2. Ingrese el desarrollador en la caja que se encuentra abajo.<br>
                    3. Verá la reseña de la desarroladora.
                    </font>
                    """,
         tags=["Consultas Generales"])
def developer_reviews_analysis(developer: str = Query(..., 
                                description="Desarrollador del videojuego", 
                                example='valve')):
    return f.developer_reviews_analysis(developer)


@app.get('/recomendacion_usuario',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga click en "Quiero probar".<br>
                    2. Ingrese el juego en la caja que se encuentra abajo.<br>
                    3. Muevase hacia abajo para obtener 5 recomendaciones de juegos similares.
                    </font>
                    """,
         tags=["Modelo de recomendación"])
def recomendacion_usuario(user_id: str = Query(..., 
                                    description="Nombre del juego para el cual se desea obtener recomendaciones", 
                                    example='Killing Floor')):
    resultado = f.recomendacion_usuario(user_id)
    if isinstance(resultado, str):
        # Si la función devuelve un mensaje de error, devolverlo en la respuesta JSON
        return JSONResponse(content={"mensaje": resultado})
    else:
        # Si la función devuelve una lista de recomendaciones, devolverla en la respuesta JSON
        juegos_recomendados = resultado
        return JSONResponse(content={"juegos_recomendados": juegos_recomendados})



@app.get('/user_data',
         description=""" <font color="blue">
                    1. Haga click en "Quiero probar".<br>
                    2. Ingrese id de usuario en la caja que se encuentra abajo.<br>
                    3. Muevase hacia abajo para ver los juegos más recomendados por los usuarios en ese año.
                    </font>
                    """,
         tags=["Consultas Generales"])
def userdata(user_id: str = Query(..., 
                                  description="ID del usuario para el que se desea obtener información")):
    resultado = f.userdata(user_id)
    return resultado


