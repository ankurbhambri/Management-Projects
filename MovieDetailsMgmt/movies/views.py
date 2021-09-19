import re
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
from movies.models import Movie, UserMovie


def try_or(fn, default, *args, **kwargs):
    """
    Usage: try_or(lambda: request_user.email, None, *args, **kwargs)
    """
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


class HomePageView(TemplateView):

    template_name = "movies/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {
            "movies_data": Movie.objects.all(),
            "login_user": self.request.user if self.request.user.is_authenticated else None,
        }
        return render(request, self.template_name, {"context": context})

    def post(self, request, *args, **kwargs):

        if request.POST.get('movie_search'):
            movies_data = Movie.objects.filter(
                tittle__icontains=request.POST.get('movie_search'))
            context = {
                "movies_data": movies_data,
                "login_user": self.request.user,
            }
        else:
            context = {
                "movies_data": Movie.objects.all(),
                "login_user": self.request.user,
            }
        return render(request, self.template_name, {"context": context})


class MovieDetails(DetailView):

    template_name = "movies/movie_details.html"
    model = Movie

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MovieDetails, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MovieDetails, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        whishlist = False
        watched = False
        path = self.request.get_full_path()
        query_id = re.findall('\d+', path)
        user_movie = UserMovie.objects.filter(
            user__id=request.user.id, movie__id=int(query_id[0]))
        if user_movie:
            whishlist = True
            watched_user = UserMovie.objects.filter(
                user__id=request.user.id,
                movie__id=int(query_id[0]), watched=1)
            if watched_user:
                watched = True
        context = {
            "whishlist": whishlist,
            "watched": watched,
            "erro": "",
            "movie_data": get_object_or_404(Movie, pk=kwargs['pk']),
            "login_user": self.request.user
        }
        return render(request, self.template_name, {"context": context})

    def post(self, request, *args, **kwargs):

        context = {
            "whishlist": False,
            "watched": False,
            "movie_data": get_object_or_404(Movie, pk=kwargs['pk']),
            "login_user": self.request.user
        }
        if request.POST.get('whishlist'):
            movie = Movie.objects.get(
                id=int(request.POST.get('whishlist')))
            user_whishlist = UserMovie.objects.filter(
                user__id=request.user.id, movie=movie)
            if user_whishlist:
                user_watched = UserMovie.objects.filter(
                    user__id=request.user.id, movie=movie, watched=1)
                if user_watched:
                    context.update({
                        "whishlist": True,
                        "watched": True,
                        "error": "Movie is already in WhishList"
                    })
                else:
                    context.update({
                        "whishlist": True,
                        "error": "Movie is already in WhishList"
                    })
            else:
                UserMovie.objects.create(user=request.user, movie=movie)
                context.update({
                    "whishlist": True,
                    "error": ""
                })
        else:
            movie = Movie.objects.get(
                id=int(request.POST.get('watched')))
            user_watched = UserMovie.objects.filter(
                user__id=request.user.id, movie=movie)
            if user_watched:
                if user_watched[0].watched == 1:
                    context.update({
                        "whishlist": True,
                        "watched": True,
                        "error": "Movie is already Watched"
                    })
                else:
                    user_watched[0].watched = 1
                    user_watched[0].save()
                    context.update({
                        "whishlist": True,
                        "watched": True,
                        "error": ""
                    })
        return render(request, self.template_name, {"context": context})


class WhishList(DetailView):
    template_name = "movies/whishlist.html"
    model = UserMovie

    def get(self, request, *args, **kwargs):
        user_whistlist = UserMovie.objects.filter(
            user__id=request.user.id
        ).values_list('movie', flat=True),
        context = {
            "movie_data": Movie.objects.filter(id__in=user_whistlist),
            "login_user": self.request.user
        }
        return render(request, self.template_name, {"context": context})

    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get('whistlist')
        remove_whistlist = UserMovie.objects.filter(
            user__id=request.user.id, movie__id=movie_id)
        remove_whistlist.delete()
        user_whistlist = UserMovie.objects.filter(
            user__id=request.user.id
        ).values_list('movie', flat=True),
        context = {
            "movie_data": Movie.objects.filter(id__in=user_whistlist),
            "login_user": self.request.user
        }
        return render(request, self.template_name, {"context": context})


class Watched(DetailView):
    template_name = "movies/watched.html"
    model = UserMovie

    def get(self, request, *args, **kwargs):
        user_whistlist = UserMovie.objects.filter(
            user__id=request.user.id, watched=1
        ).values_list('movie', flat=True),
        context = {
            "movie_data": Movie.objects.filter(id__in=user_whistlist),
            "login_user": self.request.user
        }
        return render(request, self.template_name, {"context": context})

    def post(self, request, *args, **kwargs):
        movie_id = request.POST.get('watched')
        remove_watched = UserMovie.objects.get(
            user__id=request.user.id, movie__id=movie_id)
        remove_watched.watched = 0
        remove_watched.save()
        user_whistlist = UserMovie.objects.filter(
            user__id=request.user.id, watched=1
        ).values_list('movie', flat=True),
        context = {
            "movie_data": Movie.objects.filter(id__in=user_whistlist),
            "login_user": self.request.user
        }
        return render(request, self.template_name, {"context": context})
