from django.core.management.base import BaseCommand  # , CommandError

from django.core.cache import caches

from core import image
from core.scraper import feed
from core.scraper import html

from blog import models
from feeder import redis

fstore = caches['feed']
istore = redis.Item()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for b in models.Blog.objects.all():
            if not b.rss:
                continue

            f = feed.Scrape(b.rss)
            if not f.ok:
                continue

            fstore.set(b.rss, {
                'host': f.host(),
                'title': f.title(),
                'image': [],
                'explain': f.description(),
            })

            for item in f.items():
                if not item.ok:
                    continue

                h = html.Scrape(item.url)
                images = image.Images(item.images())

                istore.append(b.rss, {
                    'url': item.url,
                    'title': f.title() or h.title(),
                    'explain': item.explain() or h.explain(),
                    'tags': item.tags(),
                    'images': images.better(),
                    'pictures': h.pictures(),
                    'videos': h.videos(),
                })
