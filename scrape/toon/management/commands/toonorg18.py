from django.core.management.base import BaseCommand

from core import query
from core.extractors import org18


class Command(BaseCommand):
    def handle(self, *args, **options):
        import ipdb; ipdb.set_trace()
        for p in org18.Toon().json:
            query.toon_upsert_by_org18(p)
