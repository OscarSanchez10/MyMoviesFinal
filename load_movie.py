import os
import requests
import psycopg2
from datetime import datetime, date, timezone
import sys
from dotenv import load_dotenv

load_dotenv()

def add_movie(movie_id):
    api_key = os.getenv('API_KEY')
    api_token = os.getenv('API_TOKEN')

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # Fetch movie details
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers)
    m = r.json()

    # Database connection
    conn = psycopg2.connect("dbname=django_bootstrap user=ubuntu password=thisissomeseucrepassword")
    cur = conn.cursor()

    # Check if movie already exists
    sql = 'SELECT * FROM movies_movie WHERE title = %s'
    cur.execute(sql, (m['title'],))
    movie_exists = cur.fetchall()
    if movie_exists:
        print(f"Movie '{m['title']}' already exists in the database.")
        return

    # Fetch movie credits
    r = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers)
    credits = r.json()

    actors = [(actor['name'], actor['known_for_department'], actor['id']) for actor in credits['cast'][:10]]
    crew = [(job['name'], job['job'], job['id']) for job in credits['crew'][:15]]
    credits_list = actors + crew

    # Insert or update jobs
    jobs = {job for person, job, tmdb_id in credits_list}
    cur.execute('SELECT name FROM movies_job WHERE name IN %s', (tuple(jobs),))
    jobs_in_db = {job[0] for job in cur.fetchall()}
    jobs_to_create = [(job,) for job in jobs if job not in jobs_in_db]

    if jobs_to_create:
        cur.executemany('INSERT INTO movies_job (name) VALUES (%s)', jobs_to_create)

    # Insert or update persons
    tmdb_ids = [person[2] for person in credits_list]
    cur.execute('SELECT tmdb_id FROM movies_person WHERE tmdb_id IN %s', (tuple(tmdb_ids),))
    existing_tmdb_ids = {person[0] for person in cur.fetchall()}

    # Set to track persons added in this transaction
    added_person_tmdb_ids = set()

    for person_name, person_job, person_tmdb_id in credits_list:
        if person_tmdb_id in existing_tmdb_ids or person_tmdb_id in added_person_tmdb_ids:
            print(f"Skipping person {person_name} with tmdb_id {person_tmdb_id} as it already exists.")
            continue  # Skip if the person already exists

        # Fetch person details from TMDb
        r = requests.get(f'https://api.themoviedb.org/3/person/{person_tmdb_id}?language=en-US', headers=headers)
        person_data = r.json()

        print(f"Adding person: {person_data['name']}")
        print(f"Data: {person_data}")

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

        # Add person to the set of added persons
        added_person_tmdb_ids.add(person_tmdb_id)

    # Insert or update genres
    genres = {genre['name'] for genre in m['genres']}
    cur.execute('SELECT name FROM movies_genre WHERE name IN %s', (tuple(genres),))
    genres_in_db = {genre[0] for genre in cur.fetchall()}
    genres_to_create = [(genre,) for genre in genres if genre not in genres_in_db]

    if genres_to_create:
        cur.executemany('INSERT INTO movies_genre (name) VALUES (%s)', genres_to_create)

    # Insert movie
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

    # Link movie with genres
    sql = '''
        INSERT INTO movies_movie_genres (movie_id, genre_id)
        SELECT movies_movie.id, movies_genre.id
        FROM movies_movie, movies_genre
        WHERE movies_movie.title = %s AND movies_genre.name IN %s
    '''
    cur.execute(sql, (m['title'], tuple(genres)))

    # Link movie with credits (persons and jobs)
    for person, job, tmdb_id in credits_list:
        sql = '''
            INSERT INTO movies_moviecredit (movie_id, person_id, job_id)
            SELECT movies_movie.id, movies_person.id, movies_job.id
            FROM movies_movie, movies_person, movies_job
            WHERE movies_movie.title = %s AND movies_person.tmdb_id = %s AND movies_job.name = %s
        '''
        cur.execute(sql, (m['title'], tmdb_id, job))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    add_movie(int(sys.argv[1]))
