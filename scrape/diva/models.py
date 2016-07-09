from __future__ import unicode_literals

from django.db import models

from core import models as core_models


class Diva(core_models.BaseModel):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, null=True, blank=True)
    kana = models.CharField(max_length=255)
    romaji = models.CharField(max_length=255)
    gyou = models.CharField(max_length=255)

    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    bust = models.IntegerField(null=True)
    bracup = models.CharField(max_length=255, null=True, blank=True)
    waist = models.IntegerField(null=True)
    hip = models.IntegerField(null=True)

    blood = models.IntegerField(null=True)
    birthday = models.DateField(null=True)

    class Meta:
        db_table = 'divas'
