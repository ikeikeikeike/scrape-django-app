from __future__ import unicode_literals

from django.db import models

from core.models import BaseModel


class Entry(BaseModel):
    title = models.TextField()

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
