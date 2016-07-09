import re
from os.path import join as pjoin

from django.conf import settings

from pyquery import PyQuery as pq

from core import client
from core import bracalc
from core import extractor

ENDPOINT = settings.ENDPOINTS['toonchar']

weight_ptn = re.compile(r'kg', re.IGNORECASE)
height_ptn = re.compile(r'cm', re.IGNORECASE)
bust_ptn = re.compile(r'b', re.IGNORECASE)
waist_ptn = re.compile(r'w', re.IGNORECASE)
hip_ptn = re.compile(r'h', re.IGNORECASE)


def fint(i):
    return int(float(i))


class Base(object):

    PATH = NotImplementedError('wth')

    def __init__(self, query):
        self.query = str(query)
        self._html = None

    @property
    def html(self):
        if self._html is None:
            url = self._process_url()
            self._html = client.html(url)
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
        return pjoin(ENDPOINT, self.PATH, self.query)


class Char(Base):

    PATH = 'characters'

    def info(self):
        return dict(
            product=self.product(),
            name=self.name(),
            kana=self.kana(),
            birthday=self.birthday(),
            blood=self.blood(),
            height=self.height(),
            weight=self.weight(),
            bust=self.bust(),
            waist=self.waist(),
            hip=self.hip(),
            bracup=self.bracup(),
            comment=self.comment(),
            tags=self.tags(),
        )

    def product(self):
        selector = '.profile_related a img'
        return self.doc(selector).attr('title')

    def name(self):
        selector = 'dl dt:contains(名前)'
        return self.doc(selector).next().text()

    def kana(self):
        selector = 'dl dt:contains(名前)'
        return self.doc(selector).next().attr('title')

    def birthday(self):
        selector = 'dl dt:contains(誕生日)'

        text = self.doc(selector).next().text()
        if text:
            return extractor.find_date(text)

    def blood(self):
        selector = 'dl dt:contains(血液型)'

        text = self.doc(selector).next().text()
        return text.replace('型', '')

    def height(self):
        selector = 'dl dt:contains(身長)'

        text = self.doc(selector).next().text()
        text = height_ptn.sub('', text)
        return text and fint(text)

    def weight(self):
        selector = 'dl dt:contains(体重)'

        text = self.doc(selector).next().text()
        text = weight_ptn.sub('', text)
        return text and fint(text)

    def bwh(self):
        sel = 'dl dt:contains(ｽﾘｰｻｲｽﾞ),dl dt:contains(スリーサイズ)'
        return self.doc(sel).next().text()

    def bust(self):
        bwh = self.bwh().split('/')
        if len(bwh) > 0:
            return fint(bust_ptn.sub('', bwh[0]))

    def waist(self):
        bwh = self.bwh().split('/')
        if len(bwh) > 0:
            return fint(waist_ptn.sub('', bwh[1]))

    def hip(self):
        bwh = self.bwh().split('/')
        if len(bwh) > 0:
            return fint(hip_ptn.sub('', bwh[2]))

    def bracup(self):
        h, b, w = self.height(), self.bust(), self.waist()
        if h and b and w and h > 10 and b > 10 and w > 10:
            return bracalc.calc(h, b, w)['cup']
        return ''

    def tags(self):
        selector = 'dl dt:contains(タグ)'
        doc = self.doc(selector).next()
        return [i.text() for i in doc('a').items()]

    def comment(self):
        selector = 'dl dt:contains(コメント)'
        return self.doc(selector).next().next().text()


class Toon(Base):

    PATH = 'animes'

    def info(self):
        return dict(
            name=self.name(),
            alias=self.alias(),
            author=self.author(),
            works=self.works(),
            release=self.release(),
            url=self.url(),
            tags=self.tags(),
            comment=self.comment(),
        )

    def name(self):
        selector = 'dl dt:contains(作品名)'
        return self.doc(selector).next().text()

    def alias(self):
        sel = 'dl dt:contains(通名),dl dt:contains(略称)'
        return self.doc(sel).next().text()

    def author(self):
        selector = 'dl dt:contains(原作者)'
        return self.doc(selector).next().text()

    def works(self):
        selector = 'dl dt:contains(制作会社)'
        return self.doc(selector).next().text()

    def release(self):
        selector = 'dl dt:contains(制作年)'
        text = self.doc(selector).next().text()
        if text:
            return extractor.find_date(text)

    def url(self):
        selector = 'dl dt:contains(公式サイト)'
        return self.doc(selector).next().text()

    def comment(self):
        selector = 'dl dt:contains(コメント)'
        return self.doc(selector).next().next().text()

    def tags(self):
        selector = 'dl dt:contains(タグ)'
        doc = self.doc(selector).next()
        return [i.text() for i in doc('a').items()]
