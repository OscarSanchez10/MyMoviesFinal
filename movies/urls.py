from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("actor/<int:actor_id>/", views.actor_detail, name="actor_detail"),  # Nueva URL
    path("add_review/<int:movie_id>/", views.add_review, name="add_review"),
    path("search/", views.search, name="search"), 
    path("logout/", views.logout_view, name="logout"), 
]
