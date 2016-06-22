import feedparser
from pyquery import PyQuery as pq

from core import uri
from core.elements import safe

# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0
feedparser.USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
)


class Scrape(object):
    def __init__(self, url):
        self._url = url
        self._feed = None

    def __repr__(self):
        return str(self._feed)

    @property
    def feed(self):
        if self._feed is None:
            self._feed = feedparser.parse(self._url)
        return self._feed

    @property
    def ok(self):
        return safe(self.feed, 'bozo') == 0

    def title(self):
        # TODO: Feezy get the html's title tag by pyquery when if not exists.
        return safe(self.feed, 'feed', 'title')

    def description(self):
        # TODO: Feezy get the html's description tag by pyquery when if not exists.
        return safe(self.feed, 'feed', 'subtitle')

    def image(self):
        # TODO: Feezy get the contains image in html by pyquery when if not exists.

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
        # TODO: Feezy get the html's title tag by pyquery when if not exists.
        return safe(self.item, 'title')

    def description(self):
        # TODO: Feezy get the html's description tag by pyquery when if not exists.
        return safe(self.item, 'summary')

    def tags(self):
        # TODO: Feezy get the html's keywords tag by pyquery when if not exists.
        tags = safe(self.item, 'tags')
        return tags and [safe(t['term']) for t in tags]

    def images(self):
        """
        - links: [{'href': 'http://example.com.jpg', 'rel': 'enclosure'}]
        - media_content: [{'url': 'http://example.com.jpg'}],
        - image_item: {'rdf:about': 'http://example.com.jpg'},
        - content: [{'value': '<span>egg</span><img src="http://example.com
                    .jpg" /><div><img src="http://example.ssjpg" /></div>'}]
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

        if not any(imgs):
            # TODO: Request page
            pass

        allow = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']
        return [i for i in imgs if uri.uriext(i) in allow]
