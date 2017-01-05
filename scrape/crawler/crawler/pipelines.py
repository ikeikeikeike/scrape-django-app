# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from extoon import models as exmodels
from core import models
from core.extractor import (
    safe_kana,
    safe_blood,
    safe_number,
    safe_bracup,
    safe_content
)

from crawler import items


class DjangoPipeline(object):
    def process_item(self, item, spider):

        if isinstance(item, items.Char):
            upsert_char(item)
        elif isinstance(item, items.Toon):
            upsert_toon(item)
        elif isinstance(item, items.Entry):
            upsert_entry(item)
        elif isinstance(item, items.Edmmx):
            upsert_edmmx(item)

        return item


def upsert_char(item):
    c, _ = models.Char.objects.get_or_create(name=item['name'])

    c.kana = c.kana or safe_kana(item['kana'])
    c.birthday = c.birthday or item['birthday']
    c.blood = c.blood or safe_blood(item['blood'])
    c.bust = c.bust or safe_number(item['bust'])
    c.waist = c.waist or safe_number(item['waist'])
    c.hip = c.hip or safe_number(item['hip'])
    c.bracup = c.bracup or safe_bracup(item['bracup'])
    c.height = c.height or safe_number(item['height'])
    c.weight = c.weight or safe_number(item['weight'])
    c.outline = c.outline or safe_content(item['comment'])
    c.product = c.product or item['product']

    toon = models.Toon.objects.filter(name=item['product']).first()
    if toon:
        c.toons.add(toon)

    for name in item['tags'] or []:
        tag, _ = models.Tag.objects.get_or_create(name=name)
        c.tags.add(tag)

    c.save()


def upsert_toon(item):
    t, _ = models.Toon.objects.get_or_create(name=item['name'])

    t.alias = t.alias or item['alias']
    t.url = t.url or item['url']
    t.author = t.author or item['author']
    t.works = t.works or item['works']
    t.release_date = t.release_date or item['release']
    t.outline = t.outline or item['comment']

    # TODO: make sure relative characters
    # t.chars.add()

    for name in item['tags'] or []:
        tag, _ = models.Tag.objects.get_or_create(name=name)
        t.tags.add(tag)

    t.save()


def upsert_entry(item):
    e, _ = exmodels.Entry.objects.get_or_create(title=item['title'])

    urls = [x.url for x in e.urls.all()]
    for url in filter(lambda w: w, item.get('urls', [])):
        if url not in urls:
            eu, _ = exmodels.EntryUrl.objects.get_or_create(url=url)
            e.urls.add(eu)

    codes = [x.code for x in e.codes.all()]
    for code in filter(lambda w: w, item.get('embed_codes', [])):
        if code not in codes:
            ee, _ = exmodels.EntryEmbed.objects.get_or_create(code=code)
            e.codes.add(ee)

    e.save()


def upsert_edmmx(item):
    pass
