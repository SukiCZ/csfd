from django.contrib import admin

from . import models


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'rating')
    search_fields = ('title', 'actors__name')
    list_filter = ('release_year', 'rating')
    ordering = ('-release_year', 'title')


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    list_filter = ('birth_date',)
    ordering = ('name',)
