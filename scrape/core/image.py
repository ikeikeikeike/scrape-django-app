import io

from django.core.cache import caches

import requests
from PIL import Image as IMG


cache = caches['image']


class Image(object):

    def __init__(self, uri):
        self.uri = uri
        self._image = None

    @property
    def content(self):
        content = cache.get(self.uri)
        if not content:
            content = _rq(self.uri).content
            cache.set(self.uri, content)

        return content

    @property
    def image(self):
        if not self._image:
            byte = io.BytesIO(self.content)
            self._image = IMG.open(byte)

        return self._image

    def width(self):
        return self.image.width

    def height(self):
        return self.image.height


class Urls(object):

    def __init__(self, urls):
        self.urls = urls
        self._images = []

    @property
    def images(self):
        if not self._images:
            imgs = (
                {'url': u, 'img': Image(u)}
                for u in self.urls)
            self._images = imgs

        return self._images

    def asc(self, wh='width'):
        fun = lambda i: getattr(i['img'], wh)()
        return sorted(self.images, key=fun)

    def desc(self, wh='width'):
        fun = lambda i: -getattr(i['img'], wh)()
        return sorted(self.images, key=fun)

    def better(self, limit=5):
        urls = []
        for i, img in enumerate(self.desc()):
            if i < limit:
                break
            if 500 < img['img'].width() < 1500:
                urls.append(img['url'])

        return urls


def _rq(url):
    return requests.get(url, headers={
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
            'rv:47.0) Gecko/20100101 Firefox/47.0')
    })
