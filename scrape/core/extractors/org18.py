from os.path import join as pjoin

from django.conf import settings

from core import client


ENDPOINT = settings.ENDPOINTS['org18']


class Base(object):

    PATH = NotImplementedError('wth')

    def __init__(self):
        self._json = None

    @property
    def json(self):
        if self._json is None:
            url = self._process_url()
            user = ENDPOINT['user']
            pswd = ENDPOINT['pass']

            self._json = client.json(url, auth=(user, pswd))
        return self._json

    @property
    def ok(self):
        return bool(self.json)

    def __repr__(self):
        return str(self._process_url())

    def _process_url(self):
        return pjoin(ENDPOINT['url'], self.PATH)


class Diva(Base):
    PATH = 'divas'


class Char(Base):
    PATH = 'characters'


class Toon(Base):
    PATH = 'animes'
