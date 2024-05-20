import os  # Importa el módulo os para interactuar con el sistema operativo
import requests  # Importa el módulo requests para enviar solicitudes HTTP
import psycopg2  # Importa el adaptador de base de datos PostgreSQL para Python
from datetime import datetime, date, timezone  # Importa clases para trabajar con fechas y horas
import sys  # Importa funciones y variables para manipular el intérprete de Python
from dotenv import load_dotenv  # Importa la función load_dotenv para cargar variables de entorno

load_dotenv()  # Carga las variables de entorno desde un archivo .env

def add_movie(movie_id):  # Define una función llamada add_movie que toma un argumento movie_id
    api_key = os.getenv('API_KEY')  # Obtiene la clave de la API desde las variables de entorno
    api_token = os.getenv('API_TOKEN')  # Obtiene el token de la API desde las variables de entorno

    headers = {  # Define un diccionario de encabezados para las solicitudes HTTP
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"  # Incluye el token de autorización en el encabezado
    }

    # Realiza una solicitud GET a la API de TMDb para obtener detalles de una película específica
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers)
    m = r.json()  # Convierte la respuesta de la solicitud HTTP a formato JSON y la almacena en la variable m

    # Establece una conexión con la base de datos PostgreSQL
    conn = psycopg2.connect("dbname=django_bootstrap user=ubuntu password=thisissomeseucrepassword")
    cur = conn.cursor()  # Crea un cursor para ejecutar consultas SQL

    # Consulta si la película ya existe en la base de datos
    sql = 'SELECT * FROM movies_movie WHERE title = %s'
    cur.execute(sql, (m['title'],))
    movie_exists = cur.fetchall()

    # Si la película ya existe en la base de datos, muestra un mensaje y sale de la función
    if movie_exists:
        print(f"Movie '{m['title']}' already exists in the database.")
        return

    # Realiza una solicitud GET a la API de TMDb para obtener los créditos de la película
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers)
    credits = r.json()  # Convierte la respuesta de la solicitud HTTP a formato JSON y la almacena en la variable credits

    # Extrae información de los actores y el equipo de la película
    actors = [(actor['name'], actor['known_for_department'], actor['id']) for actor in credits['cast'][:10]]
    crew = [(job['name'], job['job'], job['id']) for job in credits['crew'][:15]]
    credits_list = actors + crew

    # Consulta si los trabajos ya existen en la base de datos y los inserta si no existen
    jobs = {job for person, job, tmdb_id in credits_list}
    cur.execute('SELECT name FROM movies_job WHERE name IN %s', (tuple(jobs),))
    jobs_in_db = {job[0] for job in cur.fetchall()}
    jobs_to_create = [(job,) for job in jobs if job not in jobs_in_db]

    if jobs_to_create:
        cur.executemany('INSERT INTO movies_job (name) VALUES (%s)', jobs_to_create)

    # Consulta si las personas ya existen en la base de datos y las inserta si no existen
    tmdb_ids = [person[2] for person in credits_list]
    cur.execute('SELECT tmdb_id FROM movies_person WHERE tmdb_id IN %s', (tuple(tmdb_ids),))
    existing_tmdb_ids = {person[0] for person in cur.fetchall()}

    added_person_tmdb_ids = set()  # Crea un conjunto para almacenar las personas agregadas en esta transacción

    for person_name, person_job, person_tmdb_id in credits_list:
        if person_tmdb_id in existing_tmdb_ids or person_tmdb_id in added_person_tmdb_ids:
            print(f"Skipping person {person_name} with tmdb_id {person_tmdb_id} as it already exists.")
            continue  # Salta si la persona ya existe en la base de datos

        # Realiza una solicitud GET a la API de TMDb para obtener detalles de la persona
        r = requests.get(f'https://api.themoviedb.org/3/person/{person_tmdb_id}?language=en-US', headers=headers)
        person_data = r.json()  # Convierte la respuesta de la solicitud HTTP a formato JSON y la almacena en la variable person_data

        print(f"Adding person: {person_data['name']}")
        print(f"Data: {person_data}")

        # Inserta la persona en la base de datos
        sql = '''
            INSERT INTO movies_person (name, tmdb_id, profile_path, biography, birthday, deathday, place_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cur.execute(sql, (
            person_data['name'],
            person_data['id'],
            person_data.get('profile_path', ''),
            person_data.get('biography', ''),
            person_data.get('birthday'),
            person_data.get('deathday'),
            person_data.get('place_of_birth', '')
        ))

        # Agrega la persona al conjunto de personas agregadas
        added_person_tmdb_ids.add(person_tmdb_id)

    # Consulta si los géneros ya existen en la base de datos y los inserta si no existen
    genres = {genre['name'] for genre in m['genres']}
    cur.execute('SELECT name FROM movies_genre WHERE name IN %s', (tuple(genres),))
    genres_in_db = {genre[0] for genre in cur.fetchall()}
    genres_to_create = [(genre,) for genre in genres if genre not in genres_in_db]

    if genres_to_create:
        cur.executemany('INSERT INTO movies_genre (name) VALUES (%s)', genres_to_create)

    # Inserta la película en la base de datos
    release_date = datetime.combine(date.fromisoformat(m['release_date']), datetime.min.time()).astimezone(timezone.utc)
    movie_data = (
        m['title'], m['overview'], release_date, m['runtime'],
        m['budget'], movie_id, m['revenue'], m['poster_path']
    )
    sql = '''
        INSERT INTO movies_movie (
            title, overview, release_date, running_time,
            budget, tmdb_id, revenue, poster_path
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cur.execute(sql, movie_data)

    # Vincula la película con los géneros
    sql = '''
        INSERT INTO movies_movie_genres (movie_id, genre_id)
        SELECT movies_movie.id, movies_genre.id
        FROM movies_movie, movies_genre
        WHERE movies_movie.title = %s AND movies_genre.name IN %s
    '''
    cur.execute(sql, (m['title'], tuple(genres)))

    # Vincula la película con los créditos (personas y trabajos)
    for person, job, tmdb_id in credits_list:
        sql = '''
            INSERT INTO movies_moviecredit (movie_id, person_id, job_id)
            SELECT movies_movie.id, movies_person.id, movies_job.id
            FROM movies_movie, movies_person, movies_job
            WHERE movies_movie.title = %s AND movies_person.tmdb_id = %s AND movies_job.name = %s
        '''
        cur.execute(sql, (m['title'], tmdb_id, job))

    conn.commit()  # Confirma los cambios en la base de datos
    cur.close()  # Cierra el cursor
    conn.close()  # Cierra la conexión con la base de datos

if __name__ == "__main__":
    add_movie(int(sys.argv[1]))  # Llama a la función add_movie con el argumento proporcionado en la línea de comandos
