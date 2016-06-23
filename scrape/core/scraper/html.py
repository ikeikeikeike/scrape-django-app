from core import client


class Scrape(object):

    def __init__(self, url):
        self._url = url
        self._html = None

    def __repr__(self):
        return str(self.html)

    @property
    def html(self):
        if self._html is None:
            self._html = client.html(self._url)
        return self._html

    @property
    def ok(self):
        return bool(self.html)
