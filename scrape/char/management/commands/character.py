from django.core.management.base import BaseCommand

from core.extractors import diva
from core.extractor import (
    safe_kana,
    safe_romaji,
    separate_alias
)

from diva import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        person = diva.Person()
        objs = models.Diva.objects

        for _, people in person.all().items():
            for p in people:
                name, alias = separate_alias(p['name'])
                alias = ','.join(alias)

                d, created = objs.get_or_create(name=name, alias=alias)
                if created:
                    d.kana = safe_kana(p['yomi'])
                    d.romaji = safe_romaji(p['oto'])
                    d.gyou = p['gyou']
                    d.save()
