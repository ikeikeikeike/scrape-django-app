from os.path import join as pjoin

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


class Toonchar(CrawlSpider):
    name = 'toonchar'

    allowed_domains = [tldextract.extract(ENDPOINT).registered_domain]
    start_urls = (
        ENDPOINT,
        pjoin(ENDPOINT, "animes/rank"),
        pjoin(ENDPOINT, "characters/rank")
    )

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #  Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #  Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),

        Rule(LinkExtractor(allow=(r'animes/\d+', )), callback='parse_toon', follow=True),
        Rule(LinkExtractor(allow=(r'characters/\d+', )), callback='parse_char', follow=True),
    )

    def parse_char(self, response):
        char = toonchar.Char(response.url.split('/')[-1])
        return items.Char(char.info())

    def parse_toon(self, response):
        toon = toonchar.Toon(response.url.split('/')[-1])
        return items.Toon(toon.info())
