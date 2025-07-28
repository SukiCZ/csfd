from django.db import models


class MovieManager(models.Manager):
    def top_rated(self, limit=10):
        qs = self.get_queryset()
        return qs.order_by('-rating')[:limit]

    def for_detail_view(self):
        qs = self.get_queryset()
        return qs.prefetch_related('actors')


class ActorManager(models.Manager):
    def for_detail_view(self):
        qs = self.get_queryset()
        return qs.prefetch_related('movies')
