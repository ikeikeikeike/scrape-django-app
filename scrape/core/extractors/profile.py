import re
import json

from django.conf import settings

from pyquery import PyQuery as pq

from core import client
from core import bracalc
from core import extractor


ENDPOINT = settings.ENDPOINTS['wikiorg']


def fint(i):
    return int(float(i))


class Wikipedia(object):

    def __init__(self):
        self._doc = None

    def request(self, query):
        if self._doc is None:
            text = client.text(ENDPOINT + query)
            js = json.loads(text)

            self._doc = ""
            if 'error' not in js:
                self._doc = js['parse']['text']['*']

        return self._doc

    def birthday(self, query=None):
        dom = pq(self.request(query))
        selector = 'tr th:contains(生年月日),tr td:contains(生年月日)'

        text = dom(selector).nextAll().text()
        if text:
            return extractor.find_date(text)

    def blood(self, query=None):
        dom = pq(self.request(query))
        selector = 'tr th:contains(血液型),tr td:contains(血液型)'

        text = dom(selector).nextAll().text()
        return text.replace('型', '')

    def hw(self, query=None):
        dom = pq(self.request(query))
        selector = 'tr th:contains(体重), tr td:contains(体重)'

        for d in dom(selector).nextAll():
            t = pq(d).text()
            if 'cm' in t:
                return ''.join(t.split()).replace('cm', '').replace('kg', '')

    def height(self, query=None):
        hw = self.hw(query)
        if hw:
            try:
                return fint(hw.split('/')[0])
            except ValueError:
                pass

    def weight(self, query=None):
        hw = self.hw(query)
        if hw:
            try:
                return fint(hw.split('/')[1])
            except ValueError:
                pass

    def bwh(self, query=None):
        dom = pq(self.request(query))
        selector = 'tr th:contains(スリーサイズ), tr td:contains(スリーサイズ)'

        for d in dom(selector).nextAll():
            t = pq(d).text()
            if 'cm' in t:
                return ''.join(t.split()).replace('cm', '')

    def bust(self, query=None):
        bwh = self.bwh(query)
        if bwh:
            return fint(bwh.split('-')[0])

    def waist(self, query=None):
        bwh = self.bwh(query)
        if bwh:
            return fint(bwh.split('-')[1])

    def hip(self, query=None):
        bwh = self.bwh(query)
        if bwh:
            return fint(bwh.split('-')[2])

    def bracup(self, query=None):
        dom = pq(self.request(query))
        ptn = re.compile(r"(?:[a-z]|[A-Z]){1}")
        selector = 'tr th:contains(ブラのサイズ), tr th:contains(カップサイズ)'

        r = ""

        for d in dom(selector).nextAll():
            t = pq(d).text()
            if ptn.match(t):
                r = ''.join(ptn.findall(t)[0].split())

        if not r:
            h, b, w = self.height(), self.bust(), self.waist()
            if h and b and w and h > 10 and b > 10 and w > 10:
                r = bracalc.calc(h, b, w)['cup']

        return r
