from django.core.management.base import BaseCommand

from core import query
from core.extractors import org18


class Command(BaseCommand):
    def handle(self, *args, **options):
        for p in org18.Char().json:
            query.char_upsert_by_org18(p)
