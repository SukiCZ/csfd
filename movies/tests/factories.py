import factory
from factory.django import DjangoModelFactory

from movies import models, utils


class CreatorFactory(DjangoModelFactory):
    url = factory.Sequence(lambda n: f"/tvurce/{n}/")
    name = factory.Faker("name")
    normalized_name = factory.LazyAttribute(lambda o: utils.normalize(o.name))

    class Meta:
        model = models.Creator
        django_get_or_create = ("url",)


class MovieFactory(DjangoModelFactory):
    url = factory.Sequence(lambda n: f"/film/{n}/")
    title = factory.Faker("sentence", nb_words=3)
    normalized_title = factory.LazyAttribute(lambda o: utils.normalize(o.title))
    release_year = factory.Faker("random_int", min=1900, max=2025)
    genre = factory.Faker("word")
    rating = factory.Faker("random_int", min=90, max=99)
    poster = factory.Faker("image_url")

    class Meta:
        model = models.Movie
        django_get_or_create = ("url",)


class MovieCreatorFactory(DjangoModelFactory):
    movie = factory.SubFactory(MovieFactory)
    creator = factory.SubFactory(CreatorFactory)
    role = factory.LazyFunction(lambda: models.MovieCreator.ROLE_ACTOR)

    class Meta:
        model = models.MovieCreator
