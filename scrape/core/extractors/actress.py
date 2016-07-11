import json

from django.conf import settings

from core import client
from core import consts

ENDPOINT = settings.ENDPOINTS['actress']


class Actress(object):

    def get(self, letter):
        js = client.json(self._ujoin(letter))
        people = json.loads(js)
        return people['Actresses']

    def all(self):
        people = {}
        for letter in consts.atoz_jp:
            people.update({letter: self.get(letter)})
        return people

    def _ujoin(self, path):
        return '{}{}'.format(ENDPOINT, path)
