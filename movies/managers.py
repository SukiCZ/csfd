from django.db import models


class MovieManager(models.Manager):
    def top_rated(self, limit=10):
        """
        Returns the top-rated movies, limited to the specified number.
        """
        qs = self.get_queryset()
        return qs.order_by("-rating")[:limit]

    def search(self, query):
        """
        Search for movies by normalized title.
        """
        qs = self.get_queryset()
        return qs.filter(normalized_title__icontains=query).order_by("-rating")

    def for_detail_view(self, movie_id: int):
        """
        Get movie details for the detail view, including related creators.
        """
        qs = self.get_queryset()
        return qs.prefetch_related("movie_creators").get(pk=movie_id)


class CreatorManager(models.Manager):
    def search(self, query):
        """
        Search for creators by normalized name.
        """
        qs = self.get_queryset()
        return qs.filter(normalized_name__icontains=query).order_by("name")

    def for_detail_view(self, creator_id: int):
        """
        Get creator details for the detail view, including related movies.
        """
        qs = self.get_queryset()
        return qs.prefetch_related("movie_creators").get(pk=creator_id)
