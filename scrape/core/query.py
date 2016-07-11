from . import models
from .extractor import (
    safe_kana,
    safe_blood,
    safe_bracup,
    safe_romaji,
    safe_content,
    separate_alias
)


def diva_upsert_by_org18(params):
    p = params

    name, alias = separate_alias(p['Name'])
    alias = ','.join(alias)

    m, _ = models.Diva.objects.get_or_create(name=name, alias=alias)
    m = set_profile(m, p)

    m.save()
    return m


def char_upsert_by_org18(params):
    p = params

    m, _ = models.Toon.objects.get_or_create(name=p['Name'], alias=p['Alias'])
    m = set_profile(m, p)

    if m['AnimeId'].get('Int64'):
        toon = toon_upsert_by_org18(m['Anime'])
        if not m.chars.filter(name=toon.name, alias=toon.alias).exists():
            m.toons.add(toon)

    m.save()
    return m


def toon_upsert_by_org18(params, char=None):
    p = params

    m, _ = models.Toon.objects.get_or_create(name=p['Name'], alias=p['Alias'])

    m.kana = m.kana or safe_kana(p['Kana'])
    m.romaji = m.romaji or safe_romaji(p['Romaji'])
    m.gyou = m.gyou or p['Gyou']

    m.url = m.url or p['Url']
    m.author = m.author or p['Author']
    m.works = m.works or p['Works']

    m.release_date = m.release_date or p['ReleaseDate']  # XXX: maybe setting this needs to convert datetime
    m.outline = m.outline or safe_content(p['Outline'])

    for char_params in m['Characters']:
        char = char_upsert_by_org18(char_params)
        if not m.chars.filter(name=char.name, alias=char.alias).exists():
            m.chars.add(char)

    m.save()
    return m


def set_profile(obj, params):
    m = obj
    p = params

    m.kana = m.kana or safe_kana(p['Kana'])
    m.romaji = m.romaji or safe_romaji(p['Romaji'])
    m.gyou = m.gyou or p['Gyou']

    m.height = m.height or p['Height']
    m.weight = m.weight or p['Weight']

    m.bust = m.bust or p['Bust']
    m.bracup = m.bracup or safe_bracup(p['Bracup'])
    m.waist = m.waist or p['Waist']
    m.hip = m.hip or p['Hip']

    m.blood = m.blood or safe_blood(p['Blood'])
    m.birthday = m.birthday or p['Birthday']  # XXX: maybe setting this needs to convert datetime

    thumb = p['Icon']

    if thumb.get('Src'):
        t, created = m.thumbs.get_or_create(src=thumb['Src'])
        if created:
            t.name = thumb['Src']
            t.width = thumb['Width']
            t.height = thumb['Height']
            t.mime = thumb['Mime']
            t.ext = thumb['Ext']
            t.save()

            m.thumbs.add(t)

    for tag_params in m.get('Tags', []):
        toon = toon_upsert_by_org18(m['Anime'])
        if not m.chars.filter(name=toon.name, alias=toon.alias).exists():
            m.toons.add(toon)

    return m
