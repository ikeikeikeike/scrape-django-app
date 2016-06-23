import re

from django.conf import settings
from django.utils.html import strip_tags

import requests
import feedparser
from pyquery import PyQuery as pq

from core import uri
from core import client
from core.elements import safe


wptn = re.compile(r'\w')
requests.adapters.DEFAULT_RETRIES = 5  # Force assign(patch)
feedparser.USER_AGENT = settings.USER_AGENT['chrome']  # Force assign(patch)


class Scrape(object):
    def __init__(self, url):
        self.url = url
        self._feed = None

    def __repr__(self):
        return str(self._feed)

    @property
    def feed(self):
        if self._feed is None:
            self._feed = feedparser.parse(self.url)
        return self._feed

    @property
    def ok(self):
        return safe(self.feed, 'bozo') == 0

    def title(self):
        f = safe(self.feed, 'feed')
        s = safe(f, 'title')

        if not wptn.match(s):
            doc = pq(client.html(safe(f, 'link')) or None)
            s = doc('title').text()

        return s and strip_tags(s.strip())

    def description(self):
        f = safe(self.feed, 'feed')
        s = safe(f, 'subtitle')

        if not wptn.match(s):
            doc = pq(client.html(safe(f, 'link')) or None)
            s = doc('meta[name="description"]').attr('content')

        return s and strip_tags(s.strip())

    def image(self):
        # TODO: Fuzzy get the contains images from html using
        # pyquery when if not exists.
        #
        # some pattern
        return

    def entries(self):
        return safe(self.feed, 'entries')

    def items(self):
        return [Item(e) for e in self.entries()]


class Item(object):

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return str(self.item)

    def title(self):
        s = safe(self.item, 'title')
        if not wptn.match(s):
            doc = pq(client.html(self.item['id']) or None)
            s = doc('title').text()

        return s and strip_tags(s.strip())

    def description(self):
        s = safe(self.item, 'summary')
        if not wptn.match(s):
            doc = pq(client.html(self.item['id']) or None)
            s = doc('meta[name="description"]').attr('content')

        return s and strip_tags(s.strip())

    def tags(self):
        t = safe(self.item, 'tags')
        t = t and [safe(s['term']) for s in t]

        if not t:
            doc = pq(client.html(self.item['id']) or None)
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

        elms = safe(self.item, 'links') or []
        imgs |= set([elm.get('href') for elm in elms])

        elms = safe(self.item, 'media_content') or []
        imgs |= set([elm['url'] for elm in elms])

        url = safe(self.item, 'image_item', 'rdf:about')
        imgs |= set([url])

        elms = safe(self.item, 'content') or []
        doc = set([elm['value'] for elm in elms])

        doc = pq(''.join(map(str, doc)) or None)
        imgs |= set([i.attrib['src'] for i in doc('img')])

        doc = pq(self.item.get('summary') or None)
        imgs |= set([i.attrib['src'] for i in doc('img')])

        if not any(imgs):
            # TODO: Request page
            pass

        allow = settings.ALLOW_EXTENSIONS
        return [i for i in imgs if uri.uriext(i) in allow]


def _rq(url):
    return requests.get(url, headers={
        'User-Agent': settings.USER_AGENT['firefox']
    })
