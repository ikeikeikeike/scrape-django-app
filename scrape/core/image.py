import io

from PIL import Image as IMG

from . import client


class Image(object):

    def __init__(self, url):
        self.url = url
        self._image = None

    @property
    def content(self):
        return client.img(self.url)

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

    def __init__(self, urls):
        self.urls = urls
        self._images = []

    @property
    def images(self):
        if not self._images:
            imgs = []

            for url in self.urls:
                img = Image(url)

                if img.ok:
                    imgs.append({
                        'url': url,
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
        urls = []

        for img in self.desc():
            if limit < len(urls):
                break
            if 600 < img['img'].width() < 1600:
                urls.append(img['url'])
        if not urls:
            urls = self._better(urls, 500)
        if not urls:
            urls = self._better(urls, 400)
        if not urls:
            urls = self._better(urls, 300)
        if not urls:
            urls = self._better(urls, 200)
        if not urls:
            urls = self._better(urls, 100)
        if not urls:
            urls = self._better(urls, 0)

        return urls

    def _better(self, urls, width, limit=5):
        for img in self.desc():
            if limit < len(urls):
                break
            if width < img['img'].width():
                urls.append(img['url'])

        return urls
