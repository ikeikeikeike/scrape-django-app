import os

from django.core.management.base import BaseCommand
from django.conf import settings

from core import client
from core import models


bing = settings.ENDPOINTS['bing_image']


class Command(BaseCommand):
    def handle(self, *args, **options):
        randoms = models.Char.objects.order_by('?')[:100]
        untouch = models.Char.objects.order_by('updated_at')[:100]
        blanks = models.Char.objects.filter(bust=0).order_by('?')[:100]

        for obj in set(randoms + untouch + blanks):
            query = bing['char_query'].replace('[[[query]]]', obj.name)

            js = client.json(query, auth=bing['auth'])
            if len(js['d']['results']) < 1:
                continue

            infos = sorted(js['d']['results'], key=lambda x: -int(x['Height']))
            info = infos[0]

            dt, _ = models.CharThumb.get_or_create(assoc=obj)

            dt.src = info['MediaUrl']
            dt.name = info['Title']
            dt.width = info['Width']
            dt.height = info['Height']
            dt.mime = info['ContentType']
            _, dt.ext = os.path.splitext(dt.src)
            dt.save()
