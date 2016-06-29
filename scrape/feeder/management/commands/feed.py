from django.core.management.base import BaseCommand  # , CommandError

from core.scraper import feed
from core.scraper import html


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('poll_id', nargs='+', type=int)

    #     # Named (optional) arguments
    #     parser.add_argument(
    #         '--delete',
    #         action='store_true',
    #         dest='delete',
    #         default=False,
    #         help='Delete poll instead of closing it',
    #     )
        #  if options['delete']:

    def handle(self, *args, **options):
        scrape = feed.Scrape()
        print(scrape.description())
