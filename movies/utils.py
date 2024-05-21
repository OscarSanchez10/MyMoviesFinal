import numpy as np
# Importa la librería NumPy, la cual proporciona funciones para trabajar con arreglos y matrices.

from collections import defaultdict
# Importa la clase defaultdict del módulo collections, la cual proporciona un diccionario con valores predeterminados.

from math import sqrt
# Importa la función sqrt del módulo math, la cual calcula la raíz cuadrada de un número.

def normalize_ratings(prefs):
    # Define una función llamada normalize_ratings que toma un diccionario de calificaciones (prefs) como entrada.

    normalized_prefs = defaultdict(dict)
    # Crea un nuevo diccionario para almacenar las calificaciones normalizadas.

    for user in prefs:
        # Itera sobre cada usuario en el diccionario de calificaciones.

        ratings = prefs[user].values()
        # Obtiene todas las calificaciones del usuario actual.

        mean = np.mean(list(ratings))
        # Calcula la media de las calificaciones del usuario utilizando NumPy.

        for item in prefs[user]:
            # Itera sobre cada ítem calificado por el usuario.

            normalized_prefs[user][item] = prefs[user][item] - mean
            # Normaliza la calificación restando la media del usuario.

    return normalized_prefs
    # Devuelve el diccionario de calificaciones normalizadas.

def sim_cosine(prefs, p1, p2):
    # Define una función llamada sim_cosine que calcula la similitud de coseno entre dos usuarios.

    si = {}
    # Crea un diccionario para almacenar los ítems comunes entre los dos usuarios.

    for item in prefs[p1]:
        # Itera sobre cada ítem calificado por el primer usuario.

        if item in prefs[p2]:
            # Verifica si el ítem también ha sido calificado por el segundo usuario.

            si[item] = 1
            # Si es así, lo agrega al diccionario de ítems comunes.

    n = len(si)
    # Calcula el número de ítems comunes.

    if n == 0:
        return 0
        # Si no hay ítems comunes, devuelve 0.

    sum1 = sum([prefs[p1][it] for it in si])
    # Calcula la suma de las calificaciones del primer usuario para los ítems comunes.

    sum2 = sum([prefs[p2][it] for it in si])
    # Calcula la suma de las calificaciones del segundo usuario para los ítems comunes.

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    # Calcula la suma de los cuadrados de las calificaciones del primer usuario para los ítems comunes.

    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Calcula la suma de los cuadrados de las calificaciones del segundo usuario para los ítems comunes.

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calcula la suma del producto de las calificaciones de ambos usuarios para los ítems comunes.

    num = pSum
    # El numerador de la fórmula de similitud de coseno es igual a la suma del producto de las calificaciones.

    den = sqrt(sum1Sq) * sqrt(sum2Sq)
    # El denominador de la fórmula de similitud de coseno es igual al producto de las raíces cuadradas de las sumas de cuadrados de las calificaciones.

    if den == 0:
        return 0
        # Si el denominador es cero, devuelve 0 para evitar divisiones por cero.

    similarity = num / den
    # Calcula la similitud de coseno dividiendo el numerador por el denominador.

    print(f"Similarity between user {p1} and user {p2} (Cosine): {similarity}, common items: {n}")
    # Imprime la similitud de coseno entre los dos usuarios y el número de ítems comunes.

    return similarity
    # Devuelve la similitud de coseno entre los dos usuarios.

def get_recommendations(prefs, person, similarity=sim_cosine, min_sim=0.01):
    # Define una función llamada get_recommendations que genera recomendaciones para un usuario específico.

    totals = defaultdict(float)
    # Crea un diccionario para almacenar las puntuaciones totales de los ítems.

    simSums = defaultdict(float)
    # Crea un diccionario para almacenar las sumas de similitudes.

    scaling_factor = 1  # Factor to ensure significant weight for recommendations
    # Factor de escalado para garantizar un peso significativo para las recomendaciones.

    for other in prefs:
        # Itera sobre cada usuario en el diccionario de calificaciones.

        if other == person:
            continue
            # Salta al siguiente usuario si es el mismo que la persona para la que se están generando las recomendaciones.

        sim = similarity(prefs, person, other) * scaling_factor
        # Calcula la similitud entre la persona y el otro usuario utilizando la función de similitud proporcionada.

        if sim <= min_sim:
            print(f"Skipping user {other} for user {person} due to non-positive similarity ({sim})")
            # Si la similitud es menor o igual que el valor mínimo de similitud, omite el usuario y muestra un mensaje.

            continue
            # Salta al siguiente usuario.

        for item in prefs[other]:
            # Itera sobre cada ítem calificado por el otro usuario.

            totals[item] += prefs[other][item] * sim
            # Agrega la puntuación del ítem multiplicada por la similitud al diccionario de puntuaciones totales.

            simSums[item] += sim
            # Agrega la similitud al diccionario de sumas de similitudes.

    rankings = [(total / simSums[item], item) for item, total in totals.items() if simSums[item] != 0]
    # Calcula las clasificaciones para cada ítem dividiendo la puntuación total por la suma de similitudes correspondiente, evitando divisiones por cero.

    rankings.sort(reverse=True)
    # Ordena las clasificaciones en orden descendente.

    print(f"Rankings for user {person}: {rankings}")
    # Imprime las clasificaciones para el usuario especificado.

    return rankings
    # Devuelve las clasificaciones de los ítems recomendados para el usuario especificado.

def load_movie_ratings():
    # Define una función llamada load_movie_ratings que carga las calificaciones de las películas desde la base de datos.

    from .models import MovieReview
    # Importa el modelo MovieReview desde el módulo actual.

    prefs = defaultdict(dict)
    # Crea un diccionario para almacenar las calificaciones de las películas.

    for review in MovieReview.objects.all():
        # Itera sobre todas las revisiones de películas en la base de datos.

        prefs[review.user.id][review.movie.id] = review.rating
        # Almacena la calificación de la película para el usuario correspondiente en el diccionario de calificaciones de películas.

    print("Movie ratings loaded: ", prefs)
    # Imprime el diccionario de calificaciones de películas cargadas desde la base de datos.

    normalized_prefs = normalize_ratings(prefs)
    # Normaliza las calificaciones de las películas utilizando la función normalize_ratings.

    print("Normalized movie ratings: ", normalized_prefs)
    # Imprime el diccionario de calificaciones de películas normalizadas.

    return normalized_prefs
    # Devuelve el diccionario de calificaciones de películas normalizadas.

