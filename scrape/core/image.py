import io

from django.core.cache import caches

import requests
from PIL import Image as IMG

cache = caches['image']
requests.adapters.DEFAULT_RETRIES = 5  # Force assign(patch)


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

    @property
    def ok(self):
        try:
            self.image
        except OSError:
            return False
        return True

    def width(self):
        return self.image.width

    def height(self):
        return self.image.height


class Images(object):

    def __init__(self, uris):
        self.uris = uris
        self._images = []

    @property
    def images(self):
        if not self._images:
            imgs = []

            for uri in self.uris:
                img = Image(uri)

                if img.ok:
                    imgs.append({
                        'url': uri,
                        'img': img
                    })

            self._images = imgs
        return self._images

    def asc(self, wh='width'):
        fun = lambda i: getattr(i['img'], wh)()
        return sorted(self.images, key=fun)

    def desc(self, wh='width'):
        fun = lambda i: -getattr(i['img'], wh)()
        return sorted(self.images, key=fun)

    def better(self, limit=5):
        uris = []

        for img in self.desc():
            if limit < len(uris):
                break
            if 600 < img['img'].width() < 1600:
                uris.append(img['url'])
        if not uris:
            uris = self._better(uris, 500)
        if not uris:
            uris = self._better(uris, 400)
        if not uris:
            uris = self._better(uris, 300)
        if not uris:
            uris = self._better(uris, 200)
        if not uris:
            uris = self._better(uris, 100)
        if not uris:
            uris = self._better(uris, 0)

        return uris

    def _better(self, uris, width, limit=5):
        for img in self.desc():
            if limit < len(uris):
                break
            if width < img['img'].width():
                uris.append(img['url'])

        return uris


def _rq(url):
    return requests.get(url, headers={
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
            'rv:47.0) Gecko/20100101 Firefox/47.0')
    })
