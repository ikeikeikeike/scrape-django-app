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

from core.extractors import eoaient

from crawler import items


lockin = caches['lock_in_task']

EOAIENT = settings.ENDPOINTS['eoaient']

ENDPOINT = EOAIENT['ENDPOINT']
DIRECTIVE = EOAIENT['DIRECTIVE']
DIRECTIVE2 = EOAIENT['DIRECTIVE2']


class Eoaient(CrawlSpider):
    name = 'eoaient'

    allowed_domains = [
        tldextract.extract(ENDPOINT).registered_domain
    ]
    start_urls = [
        pjoin(ENDPOINT, DIRECTIVE2),
        pjoin(ENDPOINT, DIRECTIVE),
        ENDPOINT,
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r'.+/\d+/?$', ), deny=(r'page/\d+', )),
            callback='parse_video', follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Eoaient, self).__init__(*args, **kwargs)
        # unduplicate lock
        if not lockin.add(self.__class__.__name__, 'true', 60 * 60 * 24 * 5):
           raise exceptions.CloseSpider('already launched spider')

    def spider_closed(self, spider):
        lockin.delete(self.__class__.__name__)

    def parse_video(self, response):
        vid = eoaient.Video(response.url.split('/')[-1])
        return items.Entry(vid.info())
