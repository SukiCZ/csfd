import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from movies import models
from movies.tests.factories import MovieFactory, CreatorFactory, MovieCreatorFactory


@pytest.mark.django_db
class TestIndexView:
    def test_index_view_no_query(self, client):
        # Create some top-rated movies
        movies = MovieFactory.create_batch(3)

        response = client.get(reverse("movies:index"))

        assertTemplateUsed(response, "movies/index.html")
        assert list(response.context["movies"]) == sorted(
            movies, key=lambda m: m.rating, reverse=True
        )
        assert "creators" not in response.context

    def test_index_view_with_search_query(self, client):
        # Create movie and creator with accented names that normalize to the same search term
        movie = MovieFactory(title="Příběh žlutého motýla")
        creator = CreatorFactory(name="Jiří Žlutý")
        MovieCreatorFactory(movie=movie, creator=creator)

        # Create other movies and creators that shouldn't match
        MovieFactory(title="Modrý slon")
        CreatorFactory(name="Jan Novák")

        # Search with unaccented term
        response = client.get(reverse("movies:index") + "?query=zlut")

        assertTemplateUsed(response, "movies/index.html")
        assert list(response.context["movies"]) == [movie]
        assert list(response.context["creators"]) == [creator]
        assertContains(response, "Příběh žlutého motýla")
        assertContains(response, "Jiří Žlutý")


@pytest.mark.django_db
class TestMovieDetailView:
    def test_movie_detail_view(self, client):
        movie = MovieFactory(title="Létající čáp", release_year=2022)
        creator1 = CreatorFactory(name="František Veselý")
        creator2 = CreatorFactory(name="Marie Krásná")

        MovieCreatorFactory(
            movie=movie, creator=creator1, role=models.MovieCreator.ROLE_DIRECTOR
        )
        MovieCreatorFactory(
            movie=movie, creator=creator2, role=models.MovieCreator.ROLE_ACTOR
        )

        response = client.get(
            reverse("movies:movie_detail", kwargs={"movie_id": movie.id})
        )

        assertTemplateUsed(response, "movies/movie_detail.html")
        assert response.context["movie"] == movie
        assert len(response.context["movie_creators"]) == 2
        assertContains(response, "Létající čáp")
        assertContains(response, "František Veselý")
        assertContains(response, "Marie Krásná")


@pytest.mark.django_db
class TestCreatorDetailView:
    def test_creator_detail_view(self, client):
        creator = CreatorFactory(name="Tomáš Řezníček")
        movie1 = MovieFactory(title="Zelená zahrada", release_year=2020)
        movie2 = MovieFactory(title="Červené jablko", release_year=2022)

        MovieCreatorFactory(
            movie=movie1, creator=creator, role=models.MovieCreator.ROLE_ACTOR
        )
        MovieCreatorFactory(
            movie=movie2, creator=creator, role=models.MovieCreator.ROLE_DIRECTOR
        )

        response = client.get(
            reverse("movies:creator_detail", kwargs={"creator_id": creator.id})
        )

        assertTemplateUsed(response, "movies/creator_detail.html")
        assert response.context["creator"] == creator
        assert len(response.context["creator_movies"]) == 2
        assertContains(response, "Tomáš Řezníček")
        assertContains(response, "Zelená zahrada")
        assertContains(response, "Červené jablko")
