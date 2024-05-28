### Proceso de Desarrollo

Antes de aplicar técnicas avanzadas de machine learning y procesamiento de lenguaje natural, se realizó una exhaustiva limpieza, transformación y normalización de los datos, documentada en tres notebooks de Jupyter, cada uno dedicado a una fuente de datos específica.

#### ETL

El proceso de extracción, transformación y carga (ETL) se llevó a cabo en las siguientes libretas:

1. **df_steam_games.ipynb**: Limpieza del archivo de juegos de Steam.
2. **df_users_review.ipynb**: Limpieza y desagregación del archivo de reseñas de usuarios.
3. **df_User_items.ipynb**: Limpieza y desagregación del archivo de información técnica de los juegos.

Para más detalles sobre la limpieza de datos, consulta el siguiente enlace: [link_limpieza](https://github.com/LautaroVergaraAmodeo97/Limpieza-Lautaro-Vergara-Amodeo)


# Funciones para consulta
Como parte de este ejercicio, se han desarrollado cinco funciones dentro de la API FastAPI para realizar consultas específicas en el conjunto de datos de Steam.

1. UserForGenre: Proporciona información del usuario con más horas por género y horas jugadas por año.
2. Best_developer_year : Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
3. developer_reviews_: Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
4.  userdata: Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
Estas funciones buscan exponer insights específicos sobre los datos que puedan ser de utilidad para otros equipos.
5. recomendacion_usuario: Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.
El desarrollo de las funciones y la construcción de sus bases se encuentra en el notebook: 7. 

Estas consultas y los merge que hicieron falta para que funcione se pueden ver en las notebooks de este repositorio con mucho más detalle ya que ahí me explayo con mucho más atención al detalle lo que voy haciendo y describiendo (explicando el uso de librerías y el por qué ese uso).

Lo que muestro en el vídeo es sobre este github :[link_repositorio](https://github.com/LautaroVergaraAmodeo97/Deploy-Primer-Proyecto---Lautaro-Vergara-Amodeo/tree/main)

Y aquí les dejo el link del vídeo del proyecto: [video](https://drive.google.com/file/d/147Pc6MWwYKGXpzAFa33bzRfYmA4Bwmhw/view?usp=sharing)


