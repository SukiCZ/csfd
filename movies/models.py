from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers

DEFAULT_IMAGE = (
    "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


class Movie(models.Model):
    title = models.CharField(_("title"), max_length=200)
    url = models.CharField(_("url"), max_length=100, unique=True)
    release_year = models.PositiveIntegerField(_("release year"))
    genre = models.CharField(_("genre"), max_length=100)
    rating = models.DecimalField(_("rating"), max_digits=6, decimal_places=4)
    poster = models.CharField(_("poster"), max_length=200, default=DEFAULT_IMAGE)

    objects = managers.MovieManager()

    class Meta:
        verbose_name = _("movie")
        verbose_name_plural = _("movies")
        ordering = ["-rating", "-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Creator(models.Model):
    name = models.CharField(_("name"), max_length=100)
    url = models.CharField(_("url"), max_length=100, unique=True)
    movies = models.ManyToManyField(
        Movie, related_name="creators", through="MovieCreator"
    )

    objects = managers.CreatorManager()

    class Meta:
        verbose_name = _("creator")
        verbose_name_plural = _("creators")
        ordering = ["name"]

    def __str__(self):
        return self.name


class MovieCreator(models.Model):
    ROLE_DIRECTOR = "DIRECTOR"
    ROLE_AUTHOR = "AUTHOR"
    ROLE_WRITER = "WRITER"
    ROLE_CINEMATOGRAPHY = "CINEMATOGRAPHY"
    ROLE_MUSIC = "MUSIC"
    ROLE_ACTOR = "ACTOR"
    ROLE_PRODUCER = "PRODUCER"
    ROLE_EDITOR = "EDITOR"
    ROLE_COSTUME_DESIGN = "COSTUME_DESIGN"

    ROLE_CHOICES = (
        (ROLE_DIRECTOR, _("Director")),
        (ROLE_AUTHOR, _("Author")),
        (ROLE_WRITER, _("Writer")),
        (ROLE_CINEMATOGRAPHY, _("Cinematography")),
        (ROLE_MUSIC, _("Music")),
        (ROLE_ACTOR, _("Actor")),
        (ROLE_PRODUCER, _("Producer")),
        (ROLE_EDITOR, _("Editor")),
        (ROLE_COSTUME_DESIGN, _("Costume Design")),
    )

    movie = models.ForeignKey(Movie, related_name="movie_creators", on_delete=models.CASCADE)
    creator = models.ForeignKey(
        Creator, related_name="movie_creators", on_delete=models.CASCADE
    )
    role = models.CharField(
        _("role"), max_length=15, choices=ROLE_CHOICES, default=ROLE_ACTOR
    )

    class Meta:
        verbose_name = _("movie creator")
        verbose_name_plural = _("movie creators")
        unique_together = ("movie", "creator", "role")
        ordering = ["movie__title", "creator__name"]

    def __str__(self):
        return f"{self.creator.name} ({self.role}) in {self.movie.title}"
