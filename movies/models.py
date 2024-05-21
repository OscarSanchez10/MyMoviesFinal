from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Genre(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    # Define el modelo Genre con un campo de nombre y un método '__str__' para representar objetos Genre como su nombre.

class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    # Define el modelo Job con un campo de nombre y un método '__str__' para representar objetos Job como su nombre.

class Person(models.Model):
    name = models.CharField(max_length=128)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    profile_path = models.URLField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name
    # Define el modelo Person con varios campos relacionados con la información personal de una persona y un método '__str__' para representar objetos Person como su nombre.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateTimeField(blank=True)
    running_time = models.IntegerField(blank=True) 
    budget = models.IntegerField(blank=True)
    tmdb_id = models.IntegerField(blank=True, unique=True, null=True)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre) 
    credits = models.ManyToManyField(Person, through="MovieCredit")

    def __str__(self):
        return self.title + " " + str(self.release_date.year)
    # Define el modelo Movie con campos relacionados con la información de una película, incluyendo una relación many-to-many con Genre y una relación many-to-many con Person a través del modelo MovieCredit.
    # También incluye un método 'average_rating' para calcular el promedio de las calificaciones de las películas y un método '__str__' para representar objetos Movie como su título y el año de lanzamiento.

    def average_rating(self):
        return self.moviereview_set.aggregate(Avg('rating'))['rating__avg'] or 0
    # Define un método 'average_rating' para calcular el promedio de las calificaciones de las películas basadas en las críticas asociadas.

class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # Define el modelo MovieCredit para representar la relación entre personas, películas y trabajos en una película.

class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    review = models.TextField(blank=True)
    # Define el modelo MovieReview para representar las críticas de las películas, incluyendo el usuario que las escribió, la película asociada, la calificación y la revisión.
