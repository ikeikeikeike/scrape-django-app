from django.core.management.base import BaseCommand

from core import models as core_models
from transfer import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        tag()
        site()
        diva()
        toon()


def site():
    qs = models.Site.objects.using('transfer').order_by('id').all()
    for obj in qs:
        md, c = core_models.Site.objects.get_or_create(domain=obj.domain)
        if c is True:
            md.name = obj.name
            md.domain = obj.domain
            #  md.url =
            #  md.rss =

            md.inserted_at = obj.created
            md.updated_at = obj.updated

            img = obj.icon
            core_models.SiteThumb.objects.create(
                assoc_id=md.id,
                name=img.name,
                src=img.src,
                ext=img.ext,
                mime=img.mime,
                width=img.width,
                height=img.height
            )

            md.save()


def char(characters):
    chars = []

    for obj in characters:
        md, c = core_models.Char.objects.get_or_create(name=obj.name)
        if c is True:
            md.name = obj.name
            #  md.alias = obj.alias
            md.kana = obj.kana
            md.romaji = obj.romaji
            md.gyou = obj.gyou

            md.height = obj.height
            md.weight = obj.weight

            md.bust = obj.bust
            md.waste = obj.waste
            md.hip = obj.hip
            md.bracup = obj.bracup

            md.birthday = obj.birthday
            md.blood = obj.blood

            #  md.outline = obj.outline
            md.product = obj.product

            md.inserted_at = obj.created
            md.updated_at = obj.updated
            #  md.icon_id =.icon_id

            try:
                img = obj.icon
                core_models.CharThumb.objects.create(
                    assoc_id=md.id,
                    name=img.name,
                    src=img.src,
                    ext=img.ext,
                    mime=img.mime,
                    width=img.width,
                    height=img.height
                )
            except models.Image.DoesNotExist:
                pass

            md.save()

        chars.append(md)

    return chars


def tag():
    qs = models.Tag.objects.using('transfer').order_by('id').all()
    for obj in qs:
        md, c = core_models.Tag.objects.get_or_create(name=obj.name)
        if c is True:
            md.name = obj.name
            md.kana = obj.kana
            md.romaji = obj.romaji

            # do not exist below
            #  md.orig = obj.orig
            #  md.gyou = obj.gyou
            #  md.outline = obj.outline

            md.inserted_at = obj.created
            md.updated_at = obj.updated

            try:
                img = obj.image
                core_models.TagThumb.objects.create(
                    assoc_id=md.id,
                    name=img.name,
                    src=img.src,
                    ext=img.ext,
                    mime=img.mime,
                    width=img.width,
                    height=img.height
                )
            except models.Image.DoesNotExist:
                pass

            md.save()


def toon():
    qs = models.Anime.objects.using('transfer').order_by('id').all()
    for obj in qs:
        md, c = core_models.Toon.objects.get_or_create(name=obj.name)
        if c is True:
            md.name = obj.name
            md.alias = obj.alias
            md.kana = obj.kana
            md.romaji = obj.romaji
            md.gyou = obj.gyou

            md.url = obj.url
            md.author = obj.author
            md.works = obj.works

            md.release_date = obj.release_date
            md.outline = obj.outline

            md.inserted_at = obj.created
            md.updated_at = obj.updated

            try:
                img = obj.icon
                core_models.ToonThumb.objects.create(
                    assoc_id=md.id,
                    name=img.name,
                    src=img.src,
                    ext=img.ext,
                    mime=img.mime,
                    width=img.width,
                    height=img.height
                )
            except models.Image.DoesNotExist:
                pass

            md.save()

        for chh in char(obj.characters.all()):
            md.chars.add(chh)

    qs = models.Character.objects.using('transfer').order_by('id').all()
    char(qs)


def diva():
    qs = models.Diva.objects.using('transfer').order_by('id').all()
    for obj in qs:
        md, c = core_models.Diva.objects.get_or_create(name=obj.name)
        if c is True:
            md.name = obj.name
            #  md.alias = obj.alias
            md.kana = obj.kana
            md.romaji = obj.romaji
            md.gyou = obj.gyou

            md.height = obj.height
            md.weight = obj.weight

            md.bust = obj.bust
            md.waste = obj.waste
            md.hip = obj.hip
            md.bracup = obj.bracup

            md.birthday = obj.birthday
            md.blood = obj.blood

            #  md.outline = obj.outline

            md.inserted_at = obj.created
            md.updated_at = obj.updated
            #  md.icon_id =.icon_id

            try:
                img = obj.icon
                core_models.DivaThumb.objects.create(
                    assoc_id=md.id,
                    name=img.name,
                    src=img.src,
                    ext=img.ext,
                    mime=img.mime,
                    width=img.width,
                    height=img.height
                )
            except models.Image.DoesNotExist:
                pass

            md.save()
