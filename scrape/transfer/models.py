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
    icon = models.ForeignKey('Image', related_name='Animes')

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
    pictures_count = models.IntegerField()
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime'


class Blog(BaseModel):
    user = models.ForeignKey('User', related_name='blogs')
    icon = models.ForeignKey('Image', related_name='blogs')

    rss = models.CharField(unique=True, max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    mediatype = models.CharField(max_length=16)
    adsensetype = models.CharField(max_length=16)
    last_modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    verify_link = models.IntegerField(blank=True, null=True)
    verify_rss = models.IntegerField(blank=True, null=True)
    verify_parts = models.IntegerField(blank=True, null=True)
    is_penalty = models.BooleanField()
    verify_book_rss = models.IntegerField(blank=True, null=True)
    verify_book_link = models.IntegerField(blank=True, null=True)
    verify_video_rss = models.IntegerField(blank=True, null=True)
    verify_video_link = models.IntegerField(blank=True, null=True)
    is_ban = models.CharField(max_length=255)

    @property
    def ex_mediatype(self):
        if not self.mediatype:
            return ''
        elif self.mediatype == 'movie':
            return 'movie'
        elif self.mediatype == 'image':
            return 'image'

    @property
    def ex_adsensetype(self):
        if not self.adsensetype:
            return ''
        elif self.adsensetype == '2d':
            return 'second_dimension'
        elif self.adsensetype == '3d':
            return 'third_dimention'

    class Meta:
        managed = False
        db_table = 'blog'


class Character(BaseModel):
    icon = models.ForeignKey('Image', related_name='characters')
    anime = models.ForeignKey('Anime', related_name='characters')

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
    pictures_count = models.IntegerField()
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'character'
        unique_together = (('product', 'name'),)


class Diva(BaseModel):
    videos = models.ManyToManyField('Video', through='VideoDiva')
    icon = models.ForeignKey('Image', related_name='divas')

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
    videos_count = models.IntegerField()
    html = models.TextField(blank=True, null=True)
    html_expire = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diva'


class Entry(BaseModel):
    blog = models.ForeignKey('Blog', related_name='entries')
    tags = models.ManyToManyField('Tag', through='EntryTag')
    images = models.ManyToManyField('Image', through='EntryImage')

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
    is_penalty = models.BooleanField()
    page_view = models.BigIntegerField()
    is_ban = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'entry'


class EntryImage(BaseModel):
    image = models.ForeignKey('Image')
    entry = models.ForeignKey('Entry')

    class Meta:
        managed = False
        db_table = 'entry_image'


class EntryTag(BaseModel):
    tag = models.ForeignKey('Tag')
    entry = models.ForeignKey('Entry')

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
    entries = models.ManyToManyField('Entry', through='EntryImage')
    picture = models.ForeignKey('Picture', related_name='images')

    name = models.CharField(max_length=255, blank=True, null=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'image'


class Picture(BaseModel):
    characters = models.ManyToManyField('Character', through='PictureCharacter')
    entry = models.ForeignKey('Entry', related_name='pictures')
    anime = models.ForeignKey('Anime', related_name='pictures')

    created = models.DateTimeField()
    updated = models.DateTimeField()
    page_view = models.BigIntegerField()
    image_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'picture'


class PictureCharacter(BaseModel):
    character = models.ForeignKey('Character')
    picture = models.ForeignKey('Picture')

    class Meta:
        managed = False
        db_table = 'picture_character'


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
    icon = models.ForeignKey('Image', related_name='Sites')

    name = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(unique=True, max_length=255)
    outline = models.TextField(blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

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
    entries = models.ManyToManyField('Entry', through='EntryTag')
    image = models.ForeignKey('Image', related_name='tags')

    name = models.CharField(unique=True, max_length=255)
    kana = models.CharField(max_length=255, blank=True, null=True)
    romaji = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

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
    divas = models.ManyToManyField('Diva', through='VideoDiva')
    entry = models.ForeignKey('Entry', related_name='videos')
    site = models.ForeignKey('Site', related_name='videos')

    url = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    duration = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    page_view = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'video'


class VideoCode(BaseModel):
    video = models.ForeignKey('Video', related_name='video_codes')

    name = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'video_code'


class VideoUrl(BaseModel):
    video = models.ForeignKey('Video', related_name='video_urls')

    name = models.CharField(max_length=255)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'video_url'


class VideoDiva(BaseModel):
    diva = models.ForeignKey('Diva')
    video = models.ForeignKey('Video')

    class Meta:
        managed = False
        db_table = 'video_diva'


class VideoMeta(BaseModel):
    video = models.ForeignKey('Video', related_name='video_metas')
    site = models.ForeignKey('Site', related_name='video_metas')

    url = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField()
    duration = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'video_meta'


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
