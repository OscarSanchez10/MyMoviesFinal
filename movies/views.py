from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Q
from .models import Movie, MovieReview, Person, Genre
from .forms import ReviewForm
from .utils import get_recommendations, load_movie_ratings
import os
from django.contrib.auth import logout
from django.contrib.auth.models import User

def get_stars(rating):
    full_stars = int(rating // 20)
    half_star = 1 if (rating % 20) >= 10 else 0
    empty_stars = 5 - full_stars - half_star
    return {
        'full': list(range(full_stars)),
        'half': list(range(half_star)),
        'empty': list(range(empty_stars))
    }

def index(request):
    recent_movies = Movie.objects.all().order_by('-release_date')[:12]
    genres = Genre.objects.all()
    genre_movies = {genre: genre.movie_set.all()[:5] for genre in genres}

    recent_movies_with_ratings = [
        {
            'movie': movie,
            'average_rating': movie.average_rating(),
            'stars': get_stars(movie.average_rating())
        }
        for movie in recent_movies
    ]

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

    prefs = load_movie_ratings()
    recommendations = []
    if request.user.is_authenticated:
        user_id = request.user.id
        user_recommendations = get_recommendations(prefs, user_id)[:12]
        recommendations = [
            {
                'movie': Movie.objects.get(id=movie_id),
                'average_rating': Movie.objects.get(id=movie_id).average_rating(),
                'stars': get_stars(Movie.objects.get(id=movie_id).average_rating())
            }
            for _, movie_id in user_recommendations
        ]
        print(recommendations)


    context = {
        'recent_movies_with_ratings': recent_movies_with_ratings,
        'genre_movies_with_ratings': genre_movies_with_ratings,
        'recommendations_with_ratings': recommendations,
    }

    return render(request, 'movies/index.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, tmdb_id=movie_id)
    credits = movie.moviecredit_set.filter(job__name="Acting")
    reviews = MovieReview.objects.filter(movie=movie).order_by('-id')[:5]  # Solo las últimas 5 reseñas
    
    running_time_hours = movie.running_time // 60
    running_time_minutes = movie.running_time % 60

    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    stars = get_stars(average_rating)

    context = {
        'movie': movie,
        'credits': credits,
        'reviews': reviews,
        'running_time_hours': running_time_hours,
        'running_time_minutes': running_time_minutes,
        'average_rating': average_rating,
        'stars': stars,
    }
    return render(request, "movies/movie_detail.html", context=context)
    
def actor_detail(request, actor_id):
    actor = get_object_or_404(Person, tmdb_id=actor_id)
    credits = actor.moviecredit_set.all()

    context = {
        'actor': actor,
        'credits': credits,
    }
    return render(request, "movies/actor_detail.html", context=context)
    
@login_required(login_url='/admin/login/')
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, tmdb_id=movie_id)

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


def search(request):
    query = request.GET.get('q')
    results = Movie.objects.filter(Q(title__icontains=query) | Q(genres__name__icontains=query)).distinct()
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'movies/search_results.html', context)
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('/admin/login/')