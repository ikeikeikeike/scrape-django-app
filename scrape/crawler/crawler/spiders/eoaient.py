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

#  from crawler import items


lockin = caches['lock_in_task']

EOAIENT = settings.ENDPOINTS['eoaient']

ENDPOINT = EOAIENT['ENDPOINT']
DIRECTIVE = EOAIENT['DIRECTIVE']


class Eoaient(CrawlSpider):
    name = 'eoaient'

    allowed_domains = [
        tldextract.extract(ENDPOINT).registered_domain
    ]
    start_urls = (
        ENDPOINT,
        pjoin(ENDPOINT, DIRECTIVE),
    )

    rules = (
        Rule(LinkExtractor(allow=(r'{}/\d+'.format(DIRECTIVE), )), callback='parse_video', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(Eoaient, self).__init__(*args, **kwargs)
        # unduplicate lock
        #  if not lockin.add(self.__class__.__name__, 'true', 60 * 60 * 24 * 15):
            #  raise exceptions.CloseSpider('already launched spider')

    def spider_closed(self, spider):
        lockin.delete(self.__class__.__name__)

    def parse_video(self, response):
        vid = eoaient.Video(response.url.split('/')[-1])

        from pprint import pprint
        pprint(vid.title())
        pprint(vid.urls())
        pprint(vid.embed_codes())
        print('-' * 80)
