# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class BaseModel(models.Model):

    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    class Meta:
        ordering = ["-id"]
        abstract = True
        managed = False


class Anime(BaseModel):
    name = models.CharField(unique=True, max_length=128)
    alias = models.CharField(max_length=128, blank=True, null=True)
    kana = models.CharField(max_length=128, blank=True, null=True)
    romaji = models.CharField(max_length=128, blank=True, null=True)
    gyou = models.CharField(max_length=6, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=128, blank=True, null=True)
    works = models.CharField(max_length=128, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    outline = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    icon_id = models.BigIntegerField(unique=True, blank=True, null=True)
    pictures_count = models.IntegerField()
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime'


class Blog(BaseModel):
    rss = models.CharField(unique=True, max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    mediatype = models.CharField(max_length=16)
    adsensetype = models.CharField(max_length=16)
    last_modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    user_id = models.BigIntegerField(blank=True, null=True)
    icon_id = models.BigIntegerField(unique=True, blank=True, null=True)
    verify_link = models.IntegerField(blank=True, null=True)
    verify_rss = models.IntegerField(blank=True, null=True)
    verify_parts = models.IntegerField(blank=True, null=True)
    is_penalty = models.BooleanField()
    verify_book_rss = models.IntegerField(blank=True, null=True)
    verify_book_link = models.IntegerField(blank=True, null=True)
    verify_video_rss = models.IntegerField(blank=True, null=True)
    verify_video_link = models.IntegerField(blank=True, null=True)
    is_ban = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'blog'


class Character(BaseModel):
    product = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    kana = models.CharField(max_length=128, blank=True, null=True)
    romaji = models.CharField(max_length=128, blank=True, null=True)
    gyou = models.CharField(max_length=6, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    blood = models.CharField(max_length=6, blank=True, null=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    bust = models.IntegerField()
    waste = models.IntegerField()
    hip = models.IntegerField()
    bracup = models.CharField(max_length=8, blank=True, null=True)
    outline = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    icon_id = models.BigIntegerField(unique=True, blank=True, null=True)
    pictures_count = models.IntegerField()
    anime_id = models.BigIntegerField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character'
        unique_together = (('product', 'name'),)


class Diva(BaseModel):
    name = models.CharField(unique=True, max_length=128)
    kana = models.CharField(max_length=128, blank=True, null=True)
    romaji = models.CharField(max_length=128, blank=True, null=True)
    gyou = models.CharField(max_length=6, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    blood = models.CharField(max_length=6, blank=True, null=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    bust = models.IntegerField()
    waste = models.IntegerField()
    hip = models.IntegerField()
    bracup = models.CharField(max_length=8, blank=True, null=True)
    outline = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    icon_id = models.BigIntegerField(unique=True, blank=True, null=True)
    videos_count = models.IntegerField()
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diva'


class Entry(BaseModel):
    url = models.TextField()
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_content = models.TextField(blank=True, null=True)
    encoded = models.TextField(blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    q = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    blog_id = models.BigIntegerField()
    is_penalty = models.BooleanField()
    page_view = models.BigIntegerField()
    is_ban = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'entry'


class EntryImage(BaseModel):
    image_id = models.BigIntegerField()
    entry_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entry_image'


class EntryRanking(BaseModel):
    begin_name = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    rank = models.BigIntegerField()
    page_view = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    entry_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entry_ranking'
        unique_together = (('begin_name', 'begin_time', 'entry_id'),)


class EntryTag(BaseModel):
    tag_id = models.BigIntegerField()
    entry_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'entry_tag'


class GooseDbVersion(BaseModel):
    version_id = models.BigIntegerField()
    is_applied = models.BooleanField()
    tstamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goose_db_version'


class Image(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    picture_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'image'


class Picture(BaseModel):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    entry_id = models.BigIntegerField(unique=True, blank=True, null=True)
    anime_id = models.BigIntegerField(blank=True, null=True)
    page_view = models.BigIntegerField()
    image_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'picture'


class PictureCharacter(BaseModel):
    character_id = models.BigIntegerField()
    picture_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'picture_character'


class PictureRanking(BaseModel):
    begin_name = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    rank = models.BigIntegerField()
    page_view = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    picture_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'picture_ranking'
        unique_together = (('begin_name', 'begin_time', 'picture_id'),)


class Score(BaseModel):
    name = models.CharField(max_length=255)
    count = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    blog_id = models.BigIntegerField(blank=True, null=True)
    entry_id = models.BigIntegerField(blank=True, null=True)
    summary_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score'
        unique_together = (('name', 'entry_id'),)


class Site(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(unique=True, max_length=255)
    outline = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    icon_id = models.BigIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site'


class Summary(BaseModel):
    sort = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    entry_id = models.BigIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary'


class Tag(BaseModel):
    name = models.CharField(unique=True, max_length=255)
    kana = models.CharField(max_length=255, blank=True, null=True)
    romaji = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    image_id = models.BigIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class Tmpuser(BaseModel):
    rss = models.CharField(max_length=255)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=32)
    mediatype = models.CharField(max_length=16)
    adsensetype = models.CharField(max_length=16)
    using = models.CharField(max_length=32, blank=True, null=True)
    token = models.CharField(max_length=32)
    expired_at = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tmpuser'


class User(BaseModel):
    email = models.CharField(unique=True, max_length=64)
    password = models.CharField(max_length=32)
    lastlogintime = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'


class Video(BaseModel):
    url = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    entry_id = models.BigIntegerField(unique=True, blank=True, null=True)
    site_id = models.BigIntegerField(blank=True, null=True)
    page_view = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video'


class VideoCode(BaseModel):
    name = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    video_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video_code'


class VideoDiva(BaseModel):
    diva_id = models.BigIntegerField()
    video_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video_diva'


class VideoMeta(BaseModel):
    url = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField()
    duration = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    video_id = models.BigIntegerField()
    site_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_meta'


class VideoRanking(BaseModel):
    begin_name = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    rank = models.BigIntegerField()
    page_view = models.BigIntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    video_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video_ranking'
        unique_together = (('begin_name', 'begin_time', 'video_id'),)


class VideoUrl(BaseModel):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    video_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video_url'
