from decimal import Decimal

import pytest
from django.db import IntegrityError

from movies.models import Movie, MovieCreator
from movies.tests.factories import CreatorFactory, MovieCreatorFactory, MovieFactory


@pytest.mark.django_db
class TestMovieModel:
    def test_movie_creation(self, pulp_fiction):
        assert pulp_fiction.title == "Pulp Function"
        assert pulp_fiction.normalized_title == "Pulp Function"
        assert pulp_fiction.release_year == 1994
        assert pulp_fiction.rating == Decimal("91")

    def test_movie_str_representation(self, pulp_fiction):
        assert str(pulp_fiction) == "Pulp Function (1994)"

    def test_movie_ordering(self):
        # Create movies in non-sorted order to test ordering
        movie1 = MovieFactory(title="A Movie", release_year=2000, rating=Decimal("7.5"))
        movie2 = MovieFactory(title="B Movie", release_year=2010, rating=Decimal("9.0"))
        movie3 = MovieFactory(title="C Movie", release_year=2010, rating=Decimal("8.0"))

        # Django's order_by() returns a QuerySet in the specified order
        movies = Movie.objects.all()

        # Expected order: highest rating first, then release year, then title
        assert list(movies) == [movie2, movie3, movie1]


@pytest.mark.django_db
class TestCreatorModel:
    def test_creator_creation(self, quentin_tarantino):
        assert quentin_tarantino.name == "Quentin Tarantino"
        assert quentin_tarantino.normalized_name == "Quentin Tarantino"

    def test_creator_str_representation(self, quentin_tarantino):
        assert str(quentin_tarantino) == "Quentin Tarantino"


@pytest.mark.django_db
class TestMovieCreatorModel:
    def test_creator_with_multiple_roles(self, pulp_fiction, quentin_tarantino):
        # Create a movie with one creator having multiple roles
        # Create the actor role
        MovieCreatorFactory(
            movie=pulp_fiction,
            creator=quentin_tarantino,
            role=MovieCreator.ROLE_ACTOR,
        )

        # Create the director role
        MovieCreatorFactory(
            movie=pulp_fiction,
            creator=quentin_tarantino,
            role=MovieCreator.ROLE_DIRECTOR,
        )

        # Verify that the creator has both roles
        roles = MovieCreator.objects.filter(
            movie=pulp_fiction, creator=quentin_tarantino
        )
        assert roles.count() == 2
        assert set(roles.values_list("role", flat=True)) == {
            MovieCreator.ROLE_ACTOR,
            MovieCreator.ROLE_DIRECTOR,
        }

        # Verify the relationship from creator to movie
        assert quentin_tarantino in pulp_fiction.creators.all()
        assert pulp_fiction in quentin_tarantino.movies.all()

    def test_movie_creator_str_representation(self):
        movie_creator = MovieCreatorFactory()
        expected = f"{movie_creator.creator.name} ({MovieCreator.ROLE_ACTOR}) in {movie_creator.movie.title}"
        assert str(movie_creator) == expected

    def test_movie_creator_unique_constraint(self):
        # Test that we can't add the same role twice for the same creator and movie
        movie = MovieFactory()
        creator = CreatorFactory()

        MovieCreatorFactory(movie=movie, creator=creator, role=MovieCreator.ROLE_ACTOR)

        # Attempting to create the same role again should raise IntegrityError
        with pytest.raises(IntegrityError):
            MovieCreatorFactory(
                movie=movie, creator=creator, role=MovieCreator.ROLE_ACTOR
            )
