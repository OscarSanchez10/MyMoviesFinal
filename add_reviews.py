import os  # Importar el módulo os para interactuar con el sistema operativo
import django  # Importar Django para configurar el entorno
import random  # Importar random para generar calificaciones aleatorias

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymovies.settings')  # Establecer la configuración del entorno Django
django.setup()  # Configurar Django con la configuración especificada

from movies.models import Movie, MovieReview, User  # Importar los modelos necesarios de la aplicación movies

def add_reviews():
    arturo = User.objects.get(username='Arturo')  # Obtener el usuario Arturo de la base de datos
    other_users = User.objects.exclude(username='Arturo')  # Obtener todos los usuarios excepto Arturo
    movies = Movie.objects.all()  # Obtener todas las películas de la base de datos

    reviews = []  # Lista para almacenar las reseñas creadas

    # Crear reseñas para Arturo con un rango más variado de calificaciones
    for movie in movies:
        rating = random.randint(60, 100)  # Generar una calificación aleatoria para Arturo
        review_text = f"Review by Arturo with rating {rating}"  # Crear el texto de la reseña
        reviews.append(MovieReview(user=arturo, movie=movie, rating=rating, review=review_text))  # Agregar la reseña a la lista

    # Crear reseñas para otros usuarios con un rango más amplio de calificaciones
    for user in other_users:
        for movie in movies:
            rating = random.randint(20, 100)  # Generar una calificación aleatoria para otros usuarios
            review_text = f"Review by {user.username} with rating {rating}"  # Crear el texto de la reseña
            reviews.append(MovieReview(user=user, movie=movie, rating=rating, review=review_text))  # Agregar la reseña a la lista

    MovieReview.objects.bulk_create(reviews)  # Crear las reseñas en la base de datos de manera eficiente
    print("Reviews added successfully with varied ratings!")  # Imprimir un mensaje de éxito al finalizar la operación

if __name__ == '__main__':
    add_reviews()  # Llamar a la función principal si el script se ejecuta directamente
