from django.views.generic import TemplateView

from . import models
from .utils import normalize


class IndexView(TemplateView):
    template_name = "movies/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        if query:
            normalized_query = normalize(query)
            context["movies"] = models.Movie.objects.search(normalized_query)
            context["creators"] = models.Creator.objects.search(normalized_query)
        else:
            context["movies"] = models.Movie.objects.top_rated()
        return context


class MovieDetailView(TemplateView):
    template_name = "movies/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get("movie_id")
        movie = models.Movie.objects.for_detail_view(movie_id)
        context["movie"] = movie
        context["movie_creators"] = movie.movie_creators.order_by("role")
        return context


class CreatorDetailView(TemplateView):
    template_name = "movies/creator_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        creator_id = self.kwargs.get("creator_id")
        creator = models.Creator.objects.for_detail_view(creator_id)
        context["creator"] = creator
        context["creator_movies"] = creator.movie_creators.order_by(
            "role", "movie__release_year"
        )
        return context
