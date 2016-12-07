from __future__ import unicode_literals

from django.contrib.postgres import fields
from django.db import models

from core.models import BaseModel


class Entry(BaseModel):
    maker_id = models.IntegerField()  # TODO: To become foreignkey

    title = models.TextField()
    content = models.TextField()

    class Meta:
        db_table = 'entries'


class EntryUrl(BaseModel):
    entry = models.ForeignKey(Entry, related_name='urls')
    url = models.TextField()

    class Meta:
        db_table = 'entries_urls'


class EntryEmbed(BaseModel):
    entry = models.ForeignKey(Entry, related_name='codes')
    code = models.TextField()

    class Meta:
        db_table = 'entries_embeds'


class EntryInfo(BaseModel):
    assoc = models.OneToOneField(Entry, related_name='info')
    info = fields.JSONField(default=None)

    class Meta:
        db_table = 'entries_infos'
