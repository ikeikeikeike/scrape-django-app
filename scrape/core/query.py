from . import models
from .extractor import (
    safe_kana,
    safe_blood,
    safe_bracup,
    safe_romaji,
    safe_content,
    safe_datetime,
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

    m, _ = models.Char.objects.get_or_create(name=p['Name'], alias=p.get('Alias'))
    m = set_profile(m, p)

    if p['Anime'].get('Id'):
        toon = toon_upsert_by_org18(p['Anime'])
        if not m.toons.filter(name=toon.name, alias=toon.alias).exists():
            m.toons.add(toon)

    m.save()
    return m


def toon_upsert_by_org18(params, char=None):
    p = params

    m, _ = models.Toon.objects.get_or_create(name=p['Name'], alias=p['Alias'])

    m.kana = safe_kana(m.kana or p['Kana'])
    m.romaji = safe_romaji(m.romaji or p['Romaji'])
    m.gyou = m.gyou or p['Gyou']

    m.url = m.url or p['Url']
    m.author = m.author or p['Author']
    m.works = m.works or p['Works']

    m.release_date = m.release_date or safe_datetime(p['ReleaseDate'])
    m.outline = m.outline or safe_content(p['Outline'])

    add_icon(m, p)

    for char_params in p['Characters'] or []:
        char = char_upsert_by_org18(char_params)
        if not m.chars.filter(name=char.name, alias=char.alias).exists():
            m.chars.add(char)

    m.save()
    return m


def set_profile(obj, params):
    m = obj
    p = params

    m.kana = safe_kana(m.kana or p['Kana'])
    m.romaji = safe_romaji(m.romaji or p['Romaji'])
    m.gyou = m.gyou or p['Gyou']

    m.height = m.height or p['Height']
    m.weight = m.weight or p['Weight']

    m.bust = m.bust or p['Bust']
    m.bracup = safe_bracup(m.bracup or p['Bracup'])
    m.waist = m.waist or p.get('Waist', p['Waste'])
    m.hip = m.hip or p['Hip']

    m.blood = safe_blood(m.blood or p['Blood'])
    m.birthday = safe_datetime(m.birthday or p['Birthday'])

    add_icon(m, p)

    for tag_params in p.get('Tags', []):
        toon = toon_upsert_by_org18(m['Anime'])
        if not m.chars.filter(name=toon.name, alias=toon.alias).exists():
            m.toons.add(toon)

    return m


def add_icon(obj, params):
    m = obj
    p = params

    thumb = p['Icon']

    if thumb.get('Src'):
        t, _ = m.thumbs.get_or_create(src=thumb['Src'])
        t.name = thumb['Src']
        t.width = thumb['Width']
        t.height = thumb['Height']
        t.mime = thumb['Mime']
        t.ext = thumb['Ext']
        t.save()

        m.thumbs.add(t)
