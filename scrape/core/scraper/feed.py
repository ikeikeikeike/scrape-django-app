import re

from django.conf import settings
from django.utils.html import strip_tags

import feedparser
from pyquery import PyQuery as pq

from core import client
from core import extractor
from core.extractor import safe_element as selm


wptn = re.compile(r'\w')
feedparser.USER_AGENT = settings.USER_AGENT['chrome']  # Force assign(patch)


class Scrape(object):
    def __init__(self, url):
        self.url = url
        self._feed = None
        self._rq = client.html

    def __repr__(self):
        return str(self._feed)

    @property
    def feed(self):
        if self._feed is None:
            self._feed = feedparser.parse(self.url)
        return self._feed

    @property
    def ok(self):
        return selm(self.feed, 'bozo') == 0

    def title(self):
        f = selm(self.feed, 'feed')
        s = selm(f, 'title')

        if not wptn.match(s):
            doc = pq(self._rq(selm(f, 'link')) or None)
            s = doc('title').text()

        return s and strip_tags(s.strip())

    def description(self):
        f = selm(self.feed, 'feed')
        s = selm(f, 'subtitle')

        if not wptn.match(s):
            doc = pq(self._rq(selm(f, 'link')) or None)
            s = doc('meta[name="description"]').attr('content')

        return s and strip_tags(s.strip())

    def image(self):
        # TODO: Fuzzy get the contains images from html using
        # pyquery when if not exists.
        #
        # some pattern
        return

    def entries(self):
        return selm(self.feed, 'entries')

    def items(self, num=10):
        items = []
        for i, e in enumerate(self.entries()):
            if i > num:
                break

            items.append(Item(e))
        return items


class Item(object):

    def __init__(self, item):
        self.item = item
        self._rq = client.html

    def __repr__(self):
        return str(self.item)

    @property
    def ok(self):
        return bool(self._rq(self.url))

    @property
    def url(self):
        return self.item['id']

    def title(self):
        s = selm(self.item, 'title')
        if not wptn.match(s):
            doc = pq(self._rq(self.url) or None)
            s = doc('title').text()

        return s and strip_tags(s.strip())

    def description(self):
        s = selm(self.item, 'summary')
        if not wptn.match(s):
            doc = pq(self._rq(self.url) or None)
            s = doc('meta[name="description"]').attr('content')

        return s and strip_tags(s.strip())

    def tags(self):
        t = selm(self.item, 'tags')
        t = t and [selm(s['term']) for s in t]

        if not t:
            doc = pq(self._rq(self.url) or None)
            t = doc('meta[name="keywords"]').attr('content')
            t = t and t.split(',')

        return t

    def images(self):
        """
        - links: [{'href': 'http://example.com.jpg', 'rel': 'enclosure'}]
        - media_content: [{'url': 'http://example.com.jpg'}],
        - image_item: {'rdf:about': 'http://example.com.jpg'},
        - content: [{'value': '<span>egg</span><img src="http://example.com
                    .jpg" /><div><img src="http://example.ssjpg" /></div>'}]
        - summary: '<img src="http://example.ssjpg" /></div>'

        - Finally, feezy get the contains image in html when if not exists.
        """

        imgs = set()

        elms = selm(self.item, 'links') or []
        imgs |= set([elm.get('href') for elm in elms])

        elms = selm(self.item, 'media_content') or []
        imgs |= set([elm['url'] for elm in elms])

        url = selm(self.item, 'image_item', 'rdf:about')
        imgs |= set([url])

        elms = selm(self.item, 'content') or []
        doc = set([elm['value'] for elm in elms])

        doc = pq(''.join(map(str, doc)) or None)
        imgs |= set([i.attrib['src'] for i in doc('img')])

        doc = pq(self.item.get('summary') or None)
        imgs |= set([i.attrib['src'] for i in doc('img')])

        if not any(imgs):
            # XXX: Request page
            pass

        allow = settings.ALLOW_EXTENSIONS
        return [i for i in imgs if extractor.uriext(i) in allow]
