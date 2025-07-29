import asyncio

from django.core.management.base import BaseCommand

from movies.services import CSFDClient


class Command(BaseCommand):
    help = "Download data from CSFD"

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.import_data_async())
        self.stdout.write(self.style.SUCCESS("Data import completed successfully."))

    def add_arguments(self, parser):
        parser.add_argument(
            "-l," "--limit", action="store", type=int, dest="limit",
            default=300, help="Limit the number of movies to import."
        )

    async def import_data_async(self):
        await CSFDClient.scrape_catalog()
