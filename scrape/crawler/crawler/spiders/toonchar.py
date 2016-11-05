from os.path import join as pjoin

from scrapy.spiders import (
    Rule,
    CrawlSpider,
)
from scrapy import exceptions
from scrapy.linkextractors import LinkExtractor

from django.conf import settings
from django.core.cache import caches

import tldextract

from core.extractors import toonchar

from crawler import items


lockin = caches['lock_in_task']

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
        Rule(LinkExtractor(allow=(r'animes/\d+', )), callback='parse_toon', follow=True),
        Rule(LinkExtractor(allow=(r'characters/\d+', )), callback='parse_char', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(Toonchar, self).__init__(*args, **kwargs)
        # unduplicate lock
        if not lockin.add(self.__class__.__name__, 'true', 60 * 60 * 24 * 15):
            raise exceptions.CloseSpider('already launched spider')

    def spider_closed(self, spider):
        lockin.delete(self.__class__.__name__)

    def parse_char(self, response):
        char = toonchar.Char(response.url.split('/')[-1])
        return items.Char(char.info())

    def parse_toon(self, response):
        toon = toonchar.Toon(response.url.split('/')[-1])
        return items.Toon(toon.info())
