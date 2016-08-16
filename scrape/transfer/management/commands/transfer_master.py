from django.core.management.base import BaseCommand

from core import models as core_models
from transfer import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        tag()
        diva()
        char()
        toon()


def char():
    qs = models.Character.objects.using('transfer').order_by('id').all()
    for obj in qs:
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

            md.created = obj.created
            md.updated = obj.updated
            #  md.icon_id =.icon_id
            md.save()


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

            md.created = obj.created
            md.updated = obj.updated

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

            md.created = obj.created
            md.updated = obj.updated

            md.save()


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

            md.created = obj.created
            md.updated = obj.updated
            #  md.icon_id =.icon_id
            md.save()
