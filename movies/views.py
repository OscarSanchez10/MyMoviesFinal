```python
from django.shortcuts import render, get_object_or_404, redirect
# Importa funciones para renderizar plantillas, obtener objetos o redireccionar.

from django.contrib.auth.decorators import login_required
# Importa un decorador para requerir inicio de sesión.

from django.db.models import Avg,Q
# Importa funciones para calcular el promedio y realizar consultas avanzadas en modelos.

from .models import Movie, MovieReview, Person, Genre
# Importa los modelos Movie, MovieReview, Person y Genre desde el mismo directorio.

from .forms import ReviewForm
# Importa el formulario ReviewForm desde el mismo directorio.

from .utils import get_recommendations, load_movie_ratings
# Importa funciones utilitarias desde el mismo directorio.

import os
# Importa un módulo para interactuar con el sistema operativo.

from django.contrib.auth import logout
# Importa una función para cerrar sesión.

from django.contrib.auth.models import User
# Importa el modelo de usuario de Django.

def get_stars(rating):
    # Define una función para determinar las estrellas basadas en una calificación.
    full_stars = int(rating // 20)
    # Calcula el número completo de estrellas.
    half_star = 1 if (rating % 20) >= 10 else 0
    # Calcula si hay una media estrella.
    empty_stars = 5 - full_stars - half_star
    # Calcula el número de estrellas vacías.
    return {
        'full': list(range(full_stars)),
        'half': list(range(half_star)),
        'empty': list(range(empty_stars))
    }
    # Devuelve un diccionario con listas de estrellas completas, medias y vacías.

def index(request):
    # Define la vista para la página de inicio.
    recent_movies = Movie.objects.all().order_by('-release_date')[:12]
    # Obtiene las películas más recientes ordenadas por fecha de lanzamiento.
    genres = Genre.objects.all()
    # Obtiene todos los géneros.
    genre_movies = {genre: genre.movie_set.all()[:5] for genre in genres}
    # Crea un diccionario donde cada género tiene hasta 5 películas.

    recent_movies_with_ratings = [
        {
            'movie': movie,
            'average_rating': movie.average_rating(),
            'stars': get_stars(movie.average_rating())
        }
        for movie in recent_movies
    ]
    # Crea una lista de diccionarios con películas recientes y sus calificaciones promedio.

    genre_movies_with_ratings = {
        genre: [
            {
                'movie': movie,
                'average_rating': movie.average_rating(),
                'stars': get_stars(movie.average_rating())
            }
            for movie in movies
        ]
        for genre, movies in genre_movies.items()
    }
    # Crea un diccionario donde cada género tiene una lista de películas con calificaciones promedio.

    prefs = load_movie_ratings()
    # Carga las calificaciones de las películas.
    recommendations = []
    # Inicializa una lista de recomendaciones vacía.
    if request.user.is_authenticated:
        user_id = request.user.id
        # Obtiene el ID del usuario autenticado.
        user_recommendations = get_recommendations(prefs, user_id)[:12]
        # Obtiene las recomendaciones para el usuario autenticado.
        recommendations = [
            {
                'movie': Movie.objects.get(id=movie_id),
                'average_rating': Movie.objects.get(id=movie_id).average_rating(),
                'stars': get_stars(Movie.objects.get(id=movie_id).average_rating())
            }
            for _, movie_id in user_recommendations
        ]
        # Crea una lista de diccionarios con las películas recomendadas y sus calificaciones promedio.

        print(recommendations)

    context = {
        'recent_movies_with_ratings': recent_movies_with_ratings,
        'genre_movies_with_ratings': genre_movies_with_ratings,
        'recommendations_with_ratings': recommendations,
    }
    # Define el contexto para la plantilla.

    return render(request, 'movies/index.html', context)
    # Renderiza la plantilla "index.html" con el contexto proporcionado.

def movie_detail(request, movie_id):
    # Define la vista para los detalles de una película.
    movie = get_object_or_404(Movie, tmdb_id=movie_id)
    # Obtiene la película o muestra un error 404 si no se encuentra.
    credits = movie.moviecredit_set.filter(job__name="Acting")
    # Obtiene los créditos de actuación para la película.

    reviews = MovieReview.objects.filter(movie=movie).order_by('-id')[:5]
    # Obtiene las reseñas de la película ordenadas por ID, mostrando solo las últimas 5 reseñas.
    
    running_time_hours = movie.running_time // 60
    # Calcula las horas de tiempo de ejecución de la película.
    running_time_minutes = movie.running_time % 60
    # Calcula los minutos de tiempo de ejecución de la película.

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    # Calcula la calificación promedio de la película.
    stars = get_stars(average_rating)
    # Obtiene las estrellas basadas en la calificación promedio.

    context = {
        'movie': movie,
        'credits': credits,
        'reviews': reviews,
        'running_time_hours': running_time_hours,
        'running_time_minutes': running_time_minutes,
        'average_rating': average_rating,
        'stars': stars,
    }
    # Define el contexto para la plantilla.

    return render(request, "movies/movie_detail.html", context=context)
    # Renderiza la plantilla "movie_detail.html" con el contexto proporcionado.
    
def actor_detail(request, actor_id):
    # Define la vista para los detalles de un actor.
    actor = get_object_or_404(Person, tmdb_id=actor_id)
    # Obtiene el actor o muestra un error 404 si no se encuentra.
    credits = actor.moviecredit_set.all()
    # Obtiene todos los créditos del actor.

    context = {
        'actor': actor,
        'credits': credits,
    }
    # Define el contexto para la plantilla.

    return render(request, "movies/actor_detail.html", context=context)
    # Renderiza la plantilla "actor_detail.html" con el contexto proporcionado.
    
@login_required(login_url='/admin/login/')
# Requiere inicio de sesión para acceder a la vista.
def add_review(request, movie_id):
    # Define la vista para agregar una reseña a una película.
    movie = get_object_or_404(Movie, tmdb_id=movie_id)
    # Obtiene la película o muestra un error 

404 si no se encuentra.

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, "movies/add_review.html", {'form': form, 'movie': movie})
    # Renderiza la plantilla "add_review.html" con el formulario y la película proporcionados.

def search(request):
    # Define la vista para buscar películas.
    query = request.GET.get('q')
    # Obtiene el término de búsqueda de la consulta GET.
    results = Movie.objects.filter(Q(title__icontains=query) | Q(genres__name__icontains=query)).distinct()
    # Filtra las películas por título o nombre de género que coincidan con el término de búsqueda.

    context = {
        'query': query,
        'results': results,
    }
    # Define el contexto para la plantilla.

    return render(request, 'movies/search_results.html', context)
    # Renderiza la plantilla "search_results.html" con el contexto proporcionado.
    
@login_required
# Requiere inicio de sesión para acceder a la vista.
def logout_view(request):
    # Define la vista para cerrar sesión.
    logout(request)
    # Cierra la sesión del usuario.
    return redirect('/admin/login/')
    # Redirige al usuario a la página de inicio de sesión.
