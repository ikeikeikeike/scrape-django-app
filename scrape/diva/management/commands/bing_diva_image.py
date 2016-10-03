from django.core.management.base import BaseCommand
from django.conf import settings

from core import client
from core import models


bing = settings.ENDPOINTS['bing']


class Command(BaseCommand):

    def handle(self, *args, **options):

        divas = models.Diva.objects.filter().order_by('random')[:100]

        for diva in divas:
            js = client.json(bing['endpoint'] + diva.name, autn=bing['basic_auth'])
            urls = filter(lambda r: r['MediaUrl'], js['d']['results'])

            models.DivaThumb
