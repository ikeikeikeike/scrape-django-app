import json
from core import redis


class Item(redis.Base):
    name = 'item'

    def append(self, key, dct):
        return self.rdb.rpush(key, json.dumps(dct))

    def extend(self, key, dicts):
        values = [json.dumps(dct) for dct in dicts]
        return self.rdb.rpush(key, *values)

    def all(self, key):
        lrange = self.rdb.lrange(key, 0, -1)
        return [json.loads(l.decode()) for l in lrange]
