from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from movies.models import Movie
from .forms import NameForm
# Create your views here.

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
            # redirect to a new URL:
            return render(request, "movies/name_ok.html", {"form": form})
            
        else:
            return render(request, "movies/name_ok.html", {"form": form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "movies/name.html", {"form": form})
    
    

def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)
    #return HttpResponse(movies)

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie': movie}
    return render(request, "movies/movie_detail.html", context=context)
    #return HttpResponse(str(request.path))


