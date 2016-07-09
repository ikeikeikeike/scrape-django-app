import time

from django.core.management.base import BaseCommand

from core.extractors import profile
from core.extractor import (
    safe_blood,
    safe_bracup,
)

from diva import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for d in models.Diva.objects.order_by('updated_at'):
            names = [d.name] + (d.alias or '').split(',')

            for name in filter(lambda x: x, names):
                wiki = profile.Wikipedia()

                if wiki.request(name):
                    d.birthday = d.birthday or wiki.birthday()
                    d.blood = d.blood or safe_blood(wiki.blood())
                    d.bust = d.bust or wiki.bust()
                    d.waist = d.waist or wiki.waist()
                    d.hip = d.hip or wiki.hip()
                    d.bracup = d.bracup or safe_bracup(wiki.bracup())
                    d.height = d.height or wiki.height()
                    d.weight = d.weight or wiki.weight()

            d.save()
            time.sleep(60)
