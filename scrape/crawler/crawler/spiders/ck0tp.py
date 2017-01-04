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

from core.extractors import ck0tp

from crawler import items


lockin = caches['lock_in_task']

EOAIENT = settings.ENDPOINTS['ck0tp']

ENDPOINT = EOAIENT['ENDPOINT']
DIRECTIVE = EOAIENT['DIRECTIVE']


class Ck0tp(CrawlSpider):
    name = 'ck0tp'

    allowed_domains = [
        tldextract.extract(ENDPOINT).registered_domain
    ]
    start_urls = [
        pjoin(ENDPOINT, DIRECTIVE),
        ENDPOINT,
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r'archives/\d+/?$', ), deny=(r'page/\d+', )),
            callback='parse_video', follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Ck0tp, self).__init__(*args, **kwargs)
        # unduplicate lock
        if not lockin.add(self.__class__.__name__, 'true', 60 * 60 * 24 * 5):
           raise exceptions.CloseSpider('already launched spider')

    def spider_closed(self, spider):
        lockin.delete(self.__class__.__name__)

    def parse_video(self, response):
        vid = ck0tp.Video(response.url)
        return items.Entry(vid.info())
