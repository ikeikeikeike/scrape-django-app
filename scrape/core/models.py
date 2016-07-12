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
    #  user = models.ForeignKey('Users', related_name='blogs')

    name = models.CharField(max_length=255, blank=True, null=True)
    explain = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    rss = models.URLField(blank=True, null=True)

    mediatype = models.CharField(max_length=255)
    contenttype = models.CharField(max_length=255)

    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'blogs'


class Diva(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    kana = models.CharField(max_length=255, null=True, blank=True)
    romaji = models.CharField(max_length=255, null=True, blank=True)
    gyou = models.CharField(max_length=255, null=True, blank=True)

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
        unique_together = (('name', 'alias'),)


class Toon(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    kana = models.CharField(max_length=255, blank=True, null=True)
    romaji = models.CharField(max_length=255, blank=True, null=True)
    gyou = models.CharField(max_length=255, blank=True, null=True)

    url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    works = models.CharField(max_length=255, blank=True, null=True)

    release_date = models.DateTimeField(blank=True, null=True)
    outline = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField('Tag', through='ToonTag')
    chars = models.ManyToManyField('Char', through='ToonChar')

    class Meta:
        db_table = 'toons'
        unique_together = (('name', 'alias'),)


class Char(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    kana = models.CharField(max_length=255, blank=True, null=True)
    romaji = models.CharField(max_length=255, blank=True, null=True)
    gyou = models.CharField(max_length=255, blank=True, null=True)

    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)

    bust = models.IntegerField(null=True)
    bracup = models.CharField(max_length=255, blank=True, null=True)
    waist = models.IntegerField(null=True)
    hip = models.IntegerField(null=True)

    blood = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(null=True)

    tags = models.ManyToManyField('Tag', through='CharTag')
    toons = models.ManyToManyField('Toon', through='ToonChar')

    class Meta:
        db_table = 'chars'
        unique_together = (('name', 'alias'),)


class Tag(BaseModel):
    name = models.SlugField(unique=True, blank=True, null=True)
    kana = models.CharField(max_length=255, blank=True, null=True)
    romaji = models.CharField(max_length=255, blank=True, null=True)
    orig = models.CharField(max_length=255, blank=True, null=True)
    gyou = models.CharField(max_length=255, blank=True, null=True)

    chars = models.ManyToManyField('Char', through='CharTag')
    toons = models.ManyToManyField('Toon', through='ToonTag')

    class Meta:
        db_table = 'tags'


class BlogThumb(BaseModel):
    assoc = models.ForeignKey('Blog', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'blogs_thumbs'


class DivaThumb(BaseModel):
    assoc = models.ForeignKey('Diva', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'divas_thumbs'


class CharThumb(BaseModel):
    assoc = models.ForeignKey('Char', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'chars_thumbs'


class TagThumb(BaseModel):
    assoc = models.ForeignKey('Tag', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'tags_thumbs'


class ToonThumb(BaseModel):
    assoc = models.ForeignKey('Toon', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'toons_thumbs'


class ToonTag(models.Model):
    toon = models.ForeignKey('Toon')
    tag = models.ForeignKey('Tag')

    class Meta:
        managed = False
        db_table = 'toons_tags'
        unique_together = (('toon', 'tag'), ('tag', 'toon'),)


class CharTag(models.Model):
    char = models.ForeignKey('Char')
    tag = models.ForeignKey('Tag')

    class Meta:
        managed = False
        db_table = 'chars_tags'
        unique_together = (('char', 'tag'), ('tag', 'char'),)


class ToonChar(models.Model):
    toon = models.ForeignKey('Toon')
    char = models.ForeignKey('Char')

    class Meta:
        managed = False
        db_table = 'toons_chars'
        unique_together = (('toon', 'char'), ('char', 'toon'),)
