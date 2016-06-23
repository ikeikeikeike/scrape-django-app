import re
from urllib.parse import urlparse

from django.conf import settings
from django.utils.html import strip_tags

from pyquery import PyQuery as pq

from core import uri
from core import client

wptn = re.compile(r'\w')


class Scrape(object):

    def __init__(self, url):
        self.url = url
        self._html = None

    def __repr__(self):
        return str(self.html)

    @property
    def html(self):
        if self._html is None:
            self._html = client.html(self.url)
        return self._html

    @property
    def doc(self):
        return pq(self._html or None)

    @property
    def ok(self):
        return bool(self.html)

    def title(self):
        s = self.doc('title').text()
        return s and strip_tags(s.strip())

    def description(self):
        doc = self.doc('meta[name="description"]')
        s = doc.attr('content')
        return s and strip_tags(s.strip())

    def videos(self):
        return

    def images(self):
        u = urlparse(self.url)

        if "livedoor.jp" in u.netloc:
            key = u.path.split('/')[1]
            imgs = self._images(key)
        elif "fc2.com" in u.netloc:
            key = u.netloc.split('.')[0]
            imgs = self._images(key)
        else:
            parts = u.netloc.split('.')
            key = parts[len(parts) - 2]
            imgs = self._images(key)

            # for wordpress
            if len(imgs) <= 0:
                k = "wp-content/uploads"
                imgs = self._images(k)

        allow = settings.ALLOW_EXTENSIONS
        imgs = [i for i in imgs if uri.uriext(i) in allow]
        return list(set(imgs))

    def _images(self, key):
        imgs = []
        for img in self.doc("img[src*='%s']" % key):
            imgs.append(img.attrib['src'])

        return imgs
