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


class Antenna(BaseModel):
    tags = models.ManyToManyField('Tag', through='AntennaTag')
    divas = models.ManyToManyField('Diva', through='AntennaDiva')
    toons = models.ManyToManyField('Toon', through='AntennaToon')

    blog = models.ForeignKey('Blog', related_name='antennas')
    metadata = models.ForeignKey('Metadata', related_name='antennas')
    entry = models.ForeignKey('Entry', related_name='antennas')
    video = models.ForeignKey('Video', related_name='antennas')
    picture = models.ForeignKey('Picture', related_name='antennas')
    #  summary = models.ForeignKey('Summary', related_name='antennas')

    class Meta:
        db_table = 'antennas'


class Entry(BaseModel):
    class Meta:
        db_table = 'entries'


class Video(BaseModel):
    class Meta:
        db_table = 'videos'


class Picture(BaseModel):
    class Meta:
        db_table = 'pictures'

#  class Summary(BaseModel):


class VideoMetadata(BaseModel):
    video = models.ForeignKey('Video', related_name='metadatas')
    site = models.ForeignKey('Site', related_name='metadatas', null=True)

    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    embed_code = models.TextField(blank=True, null=True)
    duration = models.IntegerField(null=True)

    class Meta:
        db_table = 'video_metadatas'


class Metadata(BaseModel):
    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    seo_title = models.TextField(blank=True, null=True)
    seo_content = models.TextField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'metadatas'


class Site(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    rss = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sites'


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

    outline = models.TextField(blank=True, null=True)

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

    product = models.CharField(max_length=255)
    outline = models.TextField(blank=True, null=True)

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

    outline = models.TextField(blank=True, null=True)

    chars = models.ManyToManyField('Char', through='CharTag')
    toons = models.ManyToManyField('Toon', through='ToonTag')

    class Meta:
        db_table = 'tags'


class EntryThumb(BaseModel):
    assoc = models.ForeignKey('Entry', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'entries_thumbs'


class PictureThumb(BaseModel):
    assoc = models.ForeignKey('Picture', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'pictures_thumbs'


class VideoMetadataThumb(BaseModel):
    assoc = models.ForeignKey('VideoMetadata', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'video_metadatas_thumbs'


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


class SiteThumb(BaseModel):
    assoc = models.ForeignKey('Site', related_name='thumbs')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)

    class Meta:
        db_table = 'sites_thumbs'


class ToonTag(models.Model):
    toon = models.ForeignKey('Toon')
    tag = models.ForeignKey('Tag')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'toons_tags'
        unique_together = (('toon', 'tag'), ('tag', 'toon'),)


class CharTag(models.Model):
    char = models.ForeignKey('Char')
    tag = models.ForeignKey('Tag')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'chars_tags'
        unique_together = (('char', 'tag'), ('tag', 'char'),)


class ToonChar(models.Model):
    toon = models.ForeignKey('Toon')
    char = models.ForeignKey('Char')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'toons_chars'
        unique_together = (('toon', 'char'), ('char', 'toon'),)


class AntennaTag(models.Model):
    antenna = models.ForeignKey('Antenna')
    tag = models.ForeignKey('Tag')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'antennas_tags'
        unique_together = (('antenna', 'tag'), ('tag', 'antenna'),)


class AntennaDiva(models.Model):
    antenna = models.ForeignKey('Antenna')
    diva = models.ForeignKey('Diva')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'antennas_divas'
        unique_together = (('antenna', 'diva'), ('diva', 'antenna'),)


class AntennaToon(models.Model):
    antenna = models.ForeignKey('Antenna')
    toon = models.ForeignKey('Toon')

    class Meta:
        managed = False
        auto_created = True
        db_table = 'antennas_toons'
        unique_together = (('antenna', 'toon'), ('toon', 'antenna'),)
