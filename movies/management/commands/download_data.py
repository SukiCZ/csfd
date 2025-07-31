import asyncio
from time import perf_counter

from django.core.management.base import BaseCommand

from movies.services import CSFDClient


class Command(BaseCommand):
    help = "Download top 300 movies from CSFD leaderboard under 30 seconds."

    def handle(self, *args, **options):
        start = perf_counter()
        self.stdout.write(
            self.style.NOTICE("Starting data import from CSFD leaderboard...")
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.import_data_async())
        end = perf_counter()
        elapsed_time = end - start
        self.stdout.write(
            self.style.SUCCESS(f"Data import completed in {elapsed_time:.2f} seconds.")
        )

    async def import_data_async(self):
        await CSFDClient.scrape_catalog()
