from django.core.cache import caches

from pyquery import PyQuery as pq

from core import client

any_cache = caches['tmp_anything']


class Base(object):

    PATH = NotImplementedError('wth')

    def __init__(self, url):
        self.url = url
        self._html = None

    @property
    def html(self):
        if self._html is None:
            url = self._process_url()
            self._html = client.text(url)
        return self._html

    @property
    def doc(self):
        return pq(self.html or None)

    @property
    def ok(self):
        return bool(self.doc)

    def info(self):
        raise NotImplementedError('wth')

    def __repr__(self):
        return str(self.info())

    def _process_url(self):
        return self.url


class Video(Base):

    def info(self):
        return dict(
            title=self.title(),
            urls=self.urls(),
            embed_codes=self.embed_codes(),
        )

    def title(self):
        sel = '#page_headline'

        return self.doc(sel).html()

    def urls(self):
        sel = '.data-link li a'

        urls = []
        for doc in self.doc(sel).items():
            urls.append(doc.html())
        return urls

    def embed_codes(self):
        sel, sele = '.accordion .video-container', 'object,iframe'

        codes = []
        for doc in self.doc(sel).items():
            codes.append(str(doc(sele)))
        return codes
