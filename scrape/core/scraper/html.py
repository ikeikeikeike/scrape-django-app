import re
from urllib.parse import urlparse

from django.conf import settings
from django.utils.html import strip_tags

import tldextract as tld
from Levenshtein import ratio
from pyquery import PyQuery as pq

from core import image
from core import client
from core import detector as detor
from core import extractor as ector
from core.video import extractor as vextor
from core.video import spider as vspider

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
        return pq(self.html or None)

    @property
    def ok(self):
        return bool(self.html)

    def title(self):
        s = self.doc('title').text()
        return s and strip_tags(s.strip())

    def explain(self):
        return self.description()

    def description(self):
        s = self.doc('meta[name="description"]')
        s = s.attr('content')
        return s and strip_tags(s.strip())

    def videos(self):
        videos = []

        for name in settings.VIDEO_ELEMENTS:
            contents = []
            vext = vextor.get_extractor(name, self.url)

            if vext:
                for url in vext.extract_urls():
                    contents.append({'url': url})

                for code in vext.extract_embed_codes():
                    contents.append({'embed_code': code})

                for href in vext.extract_urls():
                    sp = vspider.get_spider(href)
                    if sp:
                        contents.append(sp.info())

            if contents:
                videos.append({name: contents})

        return videos

    def pictures(self):
        """ Ordered image """
        high, low = 3000, 500
        imgs = []

        for i in image.Images(self.images()).images:
            cond = high > i['img'].height() > low
            cond = cond and i['img'].width() > 200

            if cond:
                imgs.append(i['url'])

        return imgs

    def images(self):
        """ Ordered image """

        imgs = []
        allow = settings.ALLOW_EXTENSIONS
        key = ector.domain(self.url) or tld.extract(self.url).domain

        imgs = self._images(imgs, key)

        # for wordpress
        if detor.is_wordpress(self.url):
            imgs = self._images(imgs, "wp-content/uploads")

        imgs = [i for i in imgs if ector.uriext(i) in allow]

        # If not exists
        if not imgs:
            for img in self.doc("img"):

                src = img.attrib.get('src')
                if not src:
                    continue

                u = urlparse(src)
                if ratio(u.netloc, key) > 0.4:
                    imgs.append(src)
                elif ratio(u.path, key) > 0.4:
                    imgs.append(src)
                else:
                    i = image.Image(src)
                    if not i.ok:
                        continue

                    if i.width() > 250 and i.height() > 500:
                        imgs.append(src)
                    elif i.width() > 500 and i.height() > 300:
                        imgs.append(src)

        imgs = [i for i in imgs if ector.uriext(i) in allow]
        return imgs

    def _images(self, imgs, key):
        for img in self.doc("img[src*='%s']" % key):
            if img not in imgs:
                imgs.append(img.attrib['src'])

        return imgs
