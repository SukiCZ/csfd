import pytest

from movies import models
from movies.services import CSFDClient


@pytest.mark.asyncio
async def test_get_leaderboard(mock_aiohttp_responses, read_html_fixture):
    html_content = read_html_fixture("leaderboard_page_1.html")
    mock_aiohttp_responses.get(
        "https://www.csfd.cz/zebricky/filmy/nejlepsi/?from=1",
        body=html_content,
        status=200,
    )

    movie_urls = await CSFDClient.get_leaderboard(page_from=1)

    # Assert we extracted the expected URLs
    expected = [
        "/film/2294-vykoupeni-z-veznice-shawshank/",
        "/film/10135-forrest-gump/",
        "/film/2292-zelena-mile/",
    ]
    assert len(movie_urls) == 3
    assert all(url.startswith("/film/") for url in movie_urls)
    assert movie_urls == expected


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_get_movie(mock_aiohttp_responses, read_html_fixture):
    html_content = read_html_fixture("movie_detail_2294.html")
    mock_aiohttp_responses.get(
        "https://www.csfd.cz/film/2294-vykoupeni-z-veznice-shawshank/prehled/",
        body=html_content,
        status=200,
    )

    movie = await CSFDClient.movie("/film/2294-vykoupeni-z-veznice-shawshank/")

    # Assert we extracted the expected movie details
    assert movie.title == "Vykoupení z věznice Shawshank"
    assert movie.release_year == 1994
    assert movie.genre == "Drama / Krimi"
    assert movie.rating == 95.35442096513104
    assert movie.poster.startswith("https://image.pmgstatic.com/")
    creators_count = await movie.movie_creators.acount()
    assert creators_count == 40
    actors_count = await movie.movie_creators.filter(
        role=models.MovieCreator.ROLE_ACTOR
    ).acount()
    assert actors_count == 32
