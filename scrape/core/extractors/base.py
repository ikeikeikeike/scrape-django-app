from pyquery import PyQuery as pq

from core import client


class ExtractBase(object):

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
