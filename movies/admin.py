from django.contrib import admin

from . import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rating")
    search_fields = ("title", "actors__name")
    list_filter = ("release_year", "rating")
    ordering = ("-release_year", "title")


@admin.register(models.Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
