from django.conf import settings
from django.core.cache import caches

from core import client

from . import base

dms = settings.ENDPOINTS['dms']

any_cache = caches['tmp_anything']


class Detail(base.ExtractBase):

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
        return r and r.get('result', {}).get('items')

    def _ujoin(self, path):
        return dms['findinfo'].format(query=path)
