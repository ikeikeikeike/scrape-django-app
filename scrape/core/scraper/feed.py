import feedparser

from core.elements import safe


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
        return safe(self.feed, 'feed', 'title')

    def description(self):
        return safe(self.feed, 'feed', 'subtitle')

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
        return safe(self.item, 'title')

    def description(self):
        return safe(self.item, 'summary')

    def tags(self):
        tags = safe(self.item, 'tags')
        return tags and [safe(t['term']) for t in tags]

    def image(self):
        # 'links': [{'href': 'http://example.com.jpg', 'rel': 'enclosure'}]
        # 'media_content': [{'url': 'http://example.com.jpg'}],
        # 'image_item': {'rdf:about': 'http://example.com.jpg'},
        # 'content': [{'value': '<span>egg</span><img src="http://example.com.jpg" />'}]
        return
