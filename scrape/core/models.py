from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):

    inserted_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=False)

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True)

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    class Meta:
        ordering = ["-id"]
        abstract = True
        managed = False


class Blog(BaseModel):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rss = models.CharField(max_length=255)

    mediatype = models.CharField(max_length=255)
    contenttype = models.CharField(max_length=255)

    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'blogs'


class Diva(BaseModel):
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

    blood = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True)

    class Meta:
        db_table = 'divas'
