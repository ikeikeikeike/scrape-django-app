from __future__ import unicode_literals

from django.db import models

from core.models import BaseModel


class Author(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'authors'


class Entry(BaseModel):
    author = models.ForeignKey(Author, related_name='entries')

    tags = models.ManyToManyField('Tag', through='EntryTag')

    title = models.TextField()
    content = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    #  sort = models.IntegerField()
    #  publish = models.NullBooleanField()
    #  published_at = models.DateTimeField()

    class Meta:
        db_table = 'entries'


class EntryEmbed(BaseModel):
    entry = models.ForeignKey(Entry, related_name='codes')
    code = models.TextField()

    class Meta:
        db_table = 'entries_embeds'


class Tag(BaseModel):
    name = models.SlugField(unique=True)

    class Meta:
        db_table = 'tags'


class EntryTag(models.Model):
    entry = models.ForeignKey(Entry)
    tag = models.ForeignKey(Tag)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'entries_tags'
        unique_together = (('entry', 'tag'), ('tag', 'entry'),)


class EntryThumb(BaseModel):
    assoc = models.ForeignKey(Entry, related_name='thumbs')

    src = models.TextField()
    name = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'entries_thumbs'
