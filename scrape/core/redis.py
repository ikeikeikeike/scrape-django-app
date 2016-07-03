from django.conf import settings

import redis


class Base(object):
    name = ''

    def __init__(self):
        self._rdb = None

    @property
    def rdb(self):
        """ connect with redisdb """
        if not self._rdb:
            cfg = settings.REDISES[self.name]
            cfg = dict((k.lower(), v) for k, v in cfg.items())
            self._rdb = redis.StrictRedis(**cfg)

        return self._rdb
