import os
import django
import random

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymovies.settings')
django.setup()

from movies.models import Movie, MovieReview, User

def add_reviews():
    arturo = User.objects.get(username='Arturo')
    other_users = User.objects.exclude(username='Arturo')
    movies = Movie.objects.all()

    reviews = []

    # Crear reseñas para Arturo con un rango más variado de calificaciones
    for movie in movies:
        rating = random.randint(60, 100)  # Rango de calificaciones variadas para Arturo
        review_text = f"Review by Arturo with rating {rating}"
        reviews.append(MovieReview(user=arturo, movie=movie, rating=rating, review=review_text))

    # Crear reseñas para otros usuarios con un rango más amplio de calificaciones
    for user in other_users:
        for movie in movies:
            rating = random.randint(20, 100)  # Rango más amplio de calificaciones
            review_text = f"Review by {user.username} with rating {rating}"
            reviews.append(MovieReview(user=user, movie=movie, rating=rating, review=review_text))

    MovieReview.objects.bulk_create(reviews)
    print("Reviews added successfully with varied ratings!")

if __name__ == '__main__':
    add_reviews()
