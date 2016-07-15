import io

from PIL import Image as IMG

from . import client


class Image(object):

    def __init__(self, url):
        self.url = url
        self._image = None
        self._rq = client.img

    @property
    def content(self):
        return self._rq(self.url)

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

    def format(self):
        return self.image.format

    def info(self):
        return dict(
            ext=self.format().lower(),
            width=self.width(),
            height=self.height(),
        )


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

    def better(self, wh='width', limit=5):
        """ Not ordered image
        """
        high, low = 1600, 600
        if wh != 'width':
            high, low = 3000, 500

        urls = []

        for img in self.images:
            if limit < len(urls):
                break
            if high > getattr(img['img'], wh)() > low:
                urls.append(img['url'])
        if not urls:
            urls = self._better(urls, wh, low - 100)
        if not urls:
            urls = self._better(urls, wh, low - 200)
        if not urls:
            urls = self._better(urls, wh, low - 300)
        if not urls:
            urls = self._better(urls, wh, low - 400)
        if not urls:
            urls = self._better(urls, wh, low - 500)
        if not urls:
            urls = self._better(urls, wh, 0)

        return urls

    def _better(self, urls, wh, size, limit=5):
        for img in self.images:
            if limit < len(urls):
                break
            elif img['url'] in urls:
                continue

            if getattr(img['img'], wh)() > size:
                urls.append(img['url'])

        return urls
