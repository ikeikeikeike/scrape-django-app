from os.path import join as pjoin

from django.conf import settings

from pyquery import PyQuery as pq

from core import client

ENDPOINT = settings.ENDPOINTS['toonchar']


def fint(i):
    return int(float(i))


class Toonchar(object):

    def __init__(self, path, query):
        self.query = pjoin(path, str(query))
        self._html = None

    @property
    def html(self):
        if self._html is None:
            url = pjoin(ENDPOINT, self.query)
            self._html = client.html(url)
        return self._html

    @property
    def doc(self):
        return pq(self.html or None)

    @property
    def ok(self):
        return bool(self.doc)

    def name(self):
        import ipdb; ipdb.set_trace()
        selector = 'dl dt:contains(名前)'

        text = self.doc(selector).nextAll().text()
        return text

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
