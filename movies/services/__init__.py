import asyncio
import json

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from .. import models

ROOT_URL = "https://www.csfd.cz%(url)s"

ROLE_MAPPING = {
    "Režie": models.MovieCreator.ROLE_DIRECTOR,
    "Předloha": models.MovieCreator.ROLE_AUTHOR,
    "Scénář": models.MovieCreator.ROLE_WRITER,
    "Kamera": models.MovieCreator.ROLE_CINEMATOGRAPHY,
    "Hudba": models.MovieCreator.ROLE_MUSIC,
    "Hrají": models.MovieCreator.ROLE_ACTOR,
    "Produkce": models.MovieCreator.ROLE_PRODUCER,
    "Střih": models.MovieCreator.ROLE_EDITOR,
    "Kostýmy": models.MovieCreator.ROLE_COSTUME_DESIGN,
}


semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10


async def sem_task(scrape_task):
    async with semaphore:
        return await scrape_task


class CSFDService:
    async def scrape_catalog(self) -> list[models.Movie]:
        """
        Scrape catalog of top 300 movies and their actors
        """
        async with ClientSession() as session:
            leaderboard_results = await asyncio.gather(
                self.get_leaderboard(session, page_from=1),
                self.get_leaderboard(session, page_from=100),
                self.get_leaderboard(session, page_from=200),
            )
            movie_urls = sum(leaderboard_results, [])
            movie_tasks = [
                sem_task(self.movie(session, movie_url)) for movie_url in movie_urls
            ]
            movies = await asyncio.gather(*movie_tasks)
        return movies

    async def get_leaderboard(
        self, session: ClientSession, page_from: int = 1
    ) -> list[str]:
        """
        Return list of Movie ID from leaderboard
        :param session: aiohttp session
        :param page_from: page from (e.g. 1, 100, 200, 300)
        :return: list of Movie urls
        """
        result = []
        data = await self.request(
            session, url="/zebricky/filmy/nejlepsi/", params={"from": page_from}
        )
        soap = BeautifulSoup(data, "lxml")
        box_content = soap.find("section", class_="box")
        for article in box_content.find_all("article"):
            anchor = article.find("a", class_="film-title-name")
            result.append(anchor.get("href"))
        return result

    async def movie(self, session: ClientSession, movie_url: str) -> models.Movie:
        """
        Download movie data from CSFD by url.
        This method should be implemented to fetch movie details from CSFD.
        """
        data = await self.request(session, url=f"{movie_url}prehled/")
        soap = BeautifulSoup(data, "lxml")
        movie_node = soap.find("div", class_="main-movie-profile")
        creators = movie_node.find("div", id="creators")
        genres = movie_node.find("div", class_="genres")
        json_ld = soap.find("script", type="application/ld+json")
        json_ld = json.loads(str(json_ld.contents[0]))

        movie, _created = await models.Movie.objects.aget_or_create(
            url=movie_url,
            defaults=dict({
                "title": json_ld["name"],
                "release_year": int(json_ld["dateCreated"]),
                "genre": genres.text,
                "rating": json_ld["aggregateRating"]["ratingValue"],
                "poster": json_ld["image"],
            })
        )
        creators_nodes = [node for node in creators.find_all("div")]
        for role_key, role_value in ROLE_MAPPING.items():
            creator_node = [node for node in creators_nodes if role_key in node.text]
            if not creator_node:
                continue
            creator_node = creator_node[0]
            for creator in creator_node.find_all("a"):
                creator_url = creator.get("href")
                creator_name = creator.text.strip()
                creator_obj, _created = await models.Creator.objects.aget_or_create(
                    url=creator_url,
                    defaults=dict(name=creator_name)
                )
                await models.MovieCreator.objects.aget_or_create(
                    movie=movie,
                    creator=creator_obj,
                    role=role_value
                )
        return movie

    @staticmethod
    async def request(session: ClientSession, url: str, params: dict = None):
        """
        Make an asynchronous HTTP GET request to the specified URL with optional parameters.
        """
        url = ROOT_URL % {"url": url}
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            content = await response.read()
            return content


CSFDClient = CSFDService()
