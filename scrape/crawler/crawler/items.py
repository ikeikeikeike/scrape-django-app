# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem

from core import models


class CharItem(DjangoItem):
    django_model = models.Char


class ToonItem(DjangoItem):
    django_model = models.Toon
