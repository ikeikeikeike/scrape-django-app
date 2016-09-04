from django.core.management.base import BaseCommand

from core.extractors import actress
from core.extractor import (
    safe_kana,
    safe_romaji,
    separate_alias
)

from core import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        actresses = actress.Actress()
        objs = models.Diva.objects

        for _, acts in actresses.all().items():
            for p in acts:
                name, alias = separate_alias(p['name'])
                alias = ','.join(alias) or None

                d, created = objs.get_or_create(name=name, alias=alias)
                if created:
                    d.kana = safe_kana(p['yomi'])
                    d.romaji = safe_romaji(p['oto'])
                    d.gyou = p['gyou']
                    d.save()
