from django.conf import settings
from django.core.cache import caches

from pyquery import PyQuery as pq

from core import client

dms = settings.ENDPOINTS['dms']

any_cache = caches['tmp_anything']


class Base(object):

    PATH = NotImplementedError('wth')

    def __init__(self, url):
        self.url = str(url)
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


class Detail(Base):

    def info(self):
        return dict(
            description=self.description(),
        )

    def description(self):
        if len(self.doc('.mg-b20.lh4 p.mg-b20')) == 1:
            return self.doc('.mg-b20.lh4 p.mg-b20').text()

        if len(self.doc('.mg-b20.lh4')) == 1:
            return self.doc('.mg-b20.lh4').text()

        if len(self.doc('.summary__txt')) == 1:
            return self.doc('.summary__txt').text()

        return None


class Info(object):

    def info(self, title):
        r = client.json(self._ujoin(title))
        return r['result']['items']

    def _ujoin(self, path):
        return dms['findinfo'].format(query=path)
