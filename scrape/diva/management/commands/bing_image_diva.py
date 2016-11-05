import os

from django.core.management.base import BaseCommand
from django.conf import settings

from core import client
from core import models


bing = settings.ENDPOINTS['bing_image']


class Command(BaseCommand):
    def handle(self, *args, **options):
        randoms = models.Diva.objects.order_by('?')[:100]
        untouch = models.Diva.objects.order_by('updated_at')[:100]
        blanks = models.Diva.objects.filter(bust=0).order_by('?')[:100]

        upsert(randoms)
        upsert(untouch)
        upsert(blanks)


def upsert(qs):
    for obj in qs:
        query = bing['diva_query'].replace('[[[query]]]', obj.name)

        js = client.json(query, auth=bing['auth'])
        if js and js['d'] and len(js['d']['results']) < 1:
            continue
        try:
            infos = sorted(js['d']['results'], key=lambda x: -int(x['Height']))
        except TypeError:
             continue

        info = infos[0]
        dt, _ = models.DivaThumb.objects.get_or_create(assoc=obj)

        dt.src = info['MediaUrl']
        dt.name = info['Title']
        dt.width = info['Width']
        dt.height = info['Height']
        dt.mime = info['ContentType']
        _, dt.ext = os.path.splitext(dt.src)
        dt.save()
