from scrapy.spiders import (
    Rule,
    CrawlSpider,
)
from scrapy.linkextractors import LinkExtractor

from django.conf import settings

import tldextract

from core.extractors import toonchar

from crawler import items


ENDPOINT = settings.ENDPOINTS['toonchar']


class Char(CrawlSpider):
    name = 'char'

    allowed_domains = [tldextract.extract(ENDPOINT).registered_domain]
    start_urls = (ENDPOINT, )

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #  Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #  Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),

        Rule(LinkExtractor(allow=(r'characters/\d+', )), callback='parse_item'),
    )

    def parse_item(self, response):
        import ipdb; ipdb.set_trace()
        self.logger.info('Hi, this is an item page! %s', response.url)
        char = toonchar.Char(response.url.split('/')[-1])

        item = items.CharItem()
        item.update(char.info())
        return item
