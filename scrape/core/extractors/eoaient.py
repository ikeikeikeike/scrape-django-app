from os.path import join as pjoin

from django.conf import settings
from django.core.cache import caches

from pyquery import PyQuery as pq

from core import client

EOAIENT = settings.ENDPOINTS['eoaient']

ENDPOINT = EOAIENT['ENDPOINT']
DIRECTIVE = EOAIENT['DIRECTIVE']

any_cache = caches['tmp_anything']


class Base(object):

    PATH = NotImplementedError('wth')

    def __init__(self, query):
        self.query = str(query)
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
        return pjoin(ENDPOINT, self.PATH, self.query)


class Video(Base):

    PATH = DIRECTIVE

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
