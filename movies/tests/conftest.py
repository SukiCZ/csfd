import os
from decimal import Decimal

import django
import pytest
from aioresponses import aioresponses
from django.conf import settings


def pytest_configure():
    # Configure Django settings for tests
    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csfd.settings")
        django.setup()


@pytest.fixture
def mock_aiohttp_responses():
    """Fixture for mocking aiohttp HTTP requests."""
    with aioresponses() as m:
        yield m


@pytest.fixture
def html_fixture_path():
    """Return the path to the HTML fixtures directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "fixtures", "html")


@pytest.fixture
def read_html_fixture(html_fixture_path):
    """Helper to read HTML fixture files."""

    def _read_fixture(filename):
        with open(os.path.join(html_fixture_path, filename), "rb") as f:
            return f.read()

    return _read_fixture


@pytest.fixture
def pulp_fiction():
    """Fixture for Pulp Fiction movie."""
    from movies.tests.factories import MovieFactory

    return MovieFactory(
        title="Pulp Function",
        normalized_title="Pulp Function",
        genre="Krimi / Drama",
        release_year=1994,
        url="/film/8852/",
        rating=Decimal("91"),
    )


@pytest.fixture
def quentin_tarantino():
    """Fixture for Quentin Tarantino creator."""
    from movies.tests.factories import CreatorFactory

    return CreatorFactory(
        name="Quentin Tarantino",
        normalized_name="Quentin Tarantino",
        url="/tvurce/2120/",
    )
