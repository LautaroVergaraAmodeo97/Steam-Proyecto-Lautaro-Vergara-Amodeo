
# Importaciones
from pathlib import Path
from fastapi import Query, FastAPI
import pandas as pd
import pyarrow.parquet as pq


# Importar los DataFrames desde archivos Parquet
df_primigenio = pd.read_parquet('df_primigenio.parquet')
df_ugenre = pd.read_parquet('df_ugenre.parquet')
df_bdev = pd.read_parquet('df_bdev.parquet')
df_sentimiento = pq.read_table('df_sentimiento.parquet').to_pandas()




def inicio():
    '''
    Página de inicio que muestra una presentación.

    Returns:
    str: Código HTML que muestra la página de inicio.
    '''
    return '''
    <html>
        <head>
            <title>EJECUCION LOCAL API STEAM </title>
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
            <h1>Bienvenido a la API Steam</h1>
            <p>Esta es la página de inicio de la API de Steam para consultas de videojuegos.</p>
        </body>
    </html>
    '''



def UserForGenre(genero: str = Query(..., 
                                      description="Género de videojuegos", 
                                      example='Adventure')):
    """
    Encuentra al usuario con más horas jugadas para un género específico.

    Parameters:
    - genero (str): Género de videojuegos.

    Returns:
    - dict: Información sobre el usuario con más horas jugadas.
    """
    # Filtrar el DataFrame por el género específico
    df_genre = df_ugenre[df_ugenre['genres'] == genero]

    # Agrupar por usuario y año, sumar las horas jugadas
    grouped_df = df_genre.groupby(['user_id', 'year_release'])['playtime_forever'].sum().reset_index()

    # Encontrar al usuario con más horas jugadas
    max_user = grouped_df.loc[grouped_df['playtime_forever'].idxmax()]['user_id']

    # Filtrar el DataFrame original para obtener las horas jugadas por año del usuario máximo
    max_user_df = df_ugenre[df_ugenre['user_id'] == max_user]
    max_user_hours_by_year = max_user_df.groupby('year_release')['playtime_forever'].sum().reset_index()

    # Crear la lista de la acumulación de horas jugadas por año
    horas_jugadas_por_anio = [{"Año": int(anio), "Horas": int(horas)} for anio, horas in zip(max_user_hours_by_year['year_release'], max_user_hours_by_year['playtime_forever'])]

    # Crear el diccionario de retorno
    resultado = {"Usuario con más horas jugadas para Género " + genero: max_user, "Horas jugadas": horas_jugadas_por_anio}

    return resultado


def developer_reviews_analysis(developer: str = Query(..., 
                                                      description="Nombre del desarrollador para el que se desea realizar el análisis")):
    """
    Realiza un análisis de sentimiento de las revisiones para un desarrollador específico.

    Parameters:
    - developer (str): Nombre del desarrollador.

    Returns:
    - dict: Resultados del análisis de sentimiento.
    """
    # Filtrar el dataframe por la desarrolladora especificada
    developer_df = df_sentimiento[df_sentimiento['developer'] == developer]

    # Sumar los valores de Sentiment_Score para cada categoría
    negative_sum = developer_df[developer_df['Sentiment_Score'] == 0].shape[0]
    neutral_sum = developer_df[developer_df['Sentiment_Score'] == 1].shape[0]
    positive_sum = developer_df[developer_df['Sentiment_Score'] == 2].shape[0]

    # Crear el diccionario de salida
    result_dict = {
        developer: {
            'Negative': negative_sum,
            'Neutral': neutral_sum,
            'Positive': positive_sum
        }
    }

    return result_dict



def userdata(user_id: str = Query(..., 
                                  description="ID del usuario para el que se desea obtener información")):
    """
    Obtiene información sobre el dinero gastado, el porcentaje de recomendación y la cantidad de items para un usuario específico.

    Parameters:
    - user_id (str): ID del usuario.

    Returns:
    - dict: Información sobre el usuario.
    """
    # Filtrar el DataFrame para obtener solo los datos del usuario especificado
    user_data = df_bdev[df_bdev['user_id'] == user_id]

    # Calcular el dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    # Calcular el porcentaje de recomendación
    total_reviews = len(user_data)
    recomendaciones_positivas = user_data['recommend'].sum()
    porcentaje_recomendacion = (recomendaciones_positivas / total_reviews) * 100 if total_reviews > 0 else 0

    # Calcular la cantidad de items
    cantidad_items = user_data['item_id'].nunique()

    # Crear el diccionario de resultados
    resultado = {
        "Usuario X": user_id,
        "Dinero gastado": f"{dinero_gastado:.2f} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "cantidad de items": cantidad_items
    }

    # Devolver el diccionario en el formato deseado
    return resultado


def developer(desarrollador: str = Query(..., 
                                         description="Nombre del desarrollador para el que se desea obtener información")):
    """
    Obtiene la cantidad de items y el porcentaje de contenido Free por año según la empresa desarrolladora.

    Parameters:
    - desarrollador (str): Nombre del desarrollador.

    Returns:
    - dict: Información sobre la cantidad de items y el porcentaje de contenido Free por año.
    """
    # Filtrar el DataFrame para obtener solo los datos del desarrollador especificado
    developer_data = df_bdev[df_bdev['developer'].str.lower() == desarrollador.lower()]

    # Verificar si el DataFrame filtrado no está vacío
    if developer_data.empty:
        return f"No se encontraron datos para el desarrollador: {desarrollador}"

    # Agrupar por año y calcular la cantidad de items y el porcentaje de contenido gratuito
    grouped_data = developer_data.groupby('year_release').agg(
        cantidad_items=('item_id', 'count'),
        contenido_free_pct=('price', lambda x: (x == 0).mean() * 100)
    ).reset_index()

    # Renombrar las columnas para el formato deseado
    grouped_data.columns = ['Año', 'Cantidad de Items', 'Contenido Free']

    # Formatear el porcentaje de contenido gratuito
    grouped_data['Contenido Free'] = grouped_data['Contenido Free'].map('{:.2f}%'.format)

    # Devolver el DataFrame con el resultado
    return grouped_data



def recomendacion_usuario(user_id: str = Query(..., description="ID del usuario para el que se desean obtener recomendaciones")):
    """
    Obtiene una lista de 5 juegos recomendados para un usuario específico.

    Parameters:
    - user_id (str): ID del usuario.

    Returns:
    - list: Lista de 5 juegos recomendados.
    """
    # Verificar que el usuario existe en el DataFrame
    if user_id not in df_bdev['user_id'].values:
        return ["No se encontró el usuario con id: {}".format(user_id)]

    # Obtener los datos de los juegos revisados por el usuario
    juegos_usuario = df_bdev[df_bdev['user_id'] == user_id]

    # Verificar si el usuario tiene juegos revisados
    if juegos_usuario.empty:
        return ["El usuario con id {} no tiene juegos revisados.".format(user_id)]

    # Obtener los géneros de los juegos revisados por el usuario
    generos_usuario = juegos_usuario['genres'].unique()

    # Filtrar los juegos que coincidan con los géneros y que el usuario no haya revisado
    juegos_recomendados = df_bdev[(df_bdev['genres'].isin(generos_usuario)) & 
                                  (~df_bdev['item_id'].isin(juegos_usuario['item_id']))]

    # Verificar si hay juegos recomendados
    if juegos_recomendados.empty:
        return ["No se encontraron juegos recomendados para el usuario con id {}.".format(user_id)]

    # Ordenar los juegos por el número de recomendaciones positivas
    juegos_recomendados['positive_recommendations'] = juegos_recomendados.groupby('item_id')['recommend'].transform('sum')
    top_recomendados = juegos_recomendados.sort_values(by='positive_recommendations', ascending=False).drop_duplicates('item_id').head(5)

    # Crear la lista de juegos recomendados
    lista_recomendaciones = top_recomendados['app_name'].tolist()

    return lista_recomendaciones
