from django.contrib import admin
# Importa el módulo de administración de Django.

from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview 
# Importa los modelos del módulo 'movies.models'.

admin.site.register(Movie)
# Registra el modelo 'Movie' en el panel de administración.

admin.site.register(Genre)
# Registra el modelo 'Genre' en el panel de administración.

admin.site.register(Job)
# Registra el modelo 'Job' en el panel de administración.

admin.site.register(Person)
# Registra el modelo 'Person' en el panel de administración.

admin.site.register(MovieCredit)
# Registra el modelo 'MovieCredit' en el panel de administración.

admin.site.register(MovieReview)
# Registra el modelo 'MovieReview' en el panel de administración.
