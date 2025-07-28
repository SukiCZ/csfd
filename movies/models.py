from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers

DEFAULT_IMAGE = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


class Movie(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    release_year = models.PositiveIntegerField(_("release year"))
    director = models.CharField(_("director"), max_length=100)
    genre = models.CharField(_("genre"), max_length=50)
    rating = models.DecimalField(_("rating"), max_digits=2, decimal_places=0)
    poster = models.CharField(_("poster"), max_length=200, default=DEFAULT_IMAGE)

    objects = managers.MovieManager()

    class Meta:
        verbose_name = _("movie")
        verbose_name_plural = _("movies")
        ordering = ["-rating", "-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Actor(models.Model):
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    birth_date = models.DateField(_("birth date"), null=True, blank=True)
    photo = models.CharField(_("photo"), max_length=200, default=DEFAULT_IMAGE)

    objects = managers.ActorManager()

    class Meta:
        verbose_name = _("actor")
        verbose_name_plural = _("actors")
        ordering = ["name"]

    def __str__(self):
        return self.name
