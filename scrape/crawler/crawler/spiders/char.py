import scrapy
from scrapy.spiders import (
    Rule,
    CrawlSpider,
)
from scrapy.linkextractors import LinkExtractor

from django.conf import settings

import tldextract


ENDPOINT = settings.ENDPOINTS['toonchar']


class Char(CrawlSpider):
    name = 'char'

    allowed_domains = [tldextract.extract(ENDPOINT).domain]
    start_urls = (ENDPOINT, )

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #  Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #  Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),

        Rule(LinkExtractor(allow=(r'characters/', )), callback='parse_item'),
    )

    def parse_item(self, response):
        import ipdb; ipdb.set_trace()
        self.logger.info('Hi, this is an item page! %s', response.url)

        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
