from django.contrib import admin

from . import models


class MovieMovieCreatorInline(admin.TabularInline):
    model = models.MovieCreator
    extra = 0
    fields = ("creator", "role")
    autocomplete_fields = ("creator",)
    ordering = ("role", "creator__name")
    readonly_fields = ("creator",)


class CreatorMovieCreatorInline(admin.TabularInline):
    model = models.MovieCreator
    extra = 0
    fields = ("movie", "role")
    autocomplete_fields = ("movie",)
    ordering = ("role", "movie__title")
    readonly_fields = ("movie",)


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rating")
    search_fields = ("normalized_title",)
    inlines = (MovieMovieCreatorInline,)
    list_filter = ("release_year",)
    ordering = ("-rating",)


@admin.register(models.Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("normalized_name",)
    inlines = (CreatorMovieCreatorInline,)
    list_filter = ("movie_creators__role",)
    ordering = ("name",)
