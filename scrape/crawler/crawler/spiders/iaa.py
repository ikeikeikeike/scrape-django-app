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

from core.extractors import iaa

from crawler import items


lockin = caches['lock_in_task']

IAA = settings.ENDPOINTS['iaa']

ENDPOINT = IAA['ENDPOINT']
ENDPATH = IAA['ENDPATH']
DIRECTIVES = IAA['DIRECTIVES']


class IAASpider(CrawlSpider):
    name = "iaa"

    allowed_domains = [
        tldextract.extract(ENDPOINT).registered_domain
    ]
    start_urls = [
        ENDPOINT,
    ] + [
        pjoin(ENDPOINT, d)
        for d in DIRECTIVES
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r'{}/([a-z]|[A-Z]|[0-9])+$'.format(ENDPATH), )),
            callback='parse_video', follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(IAASpider, self).__init__(*args, **kwargs)
        # unduplicate lock
        if not lockin.add(self.__class__.__name__, 'true', 60 * 60 * 24 * 5):
            raise exceptions.CloseSpider('already launched spider')

    def closed(self, *args, **kwargs):
        lockin.delete(self.__class__.__name__)

    def parse_video(self, response):
        vid = iaa.Video(response.url)
        return items.Edmmx(vid.info())
