from django.core.management.base import BaseCommand

from core import models as core_models
from transfer import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = models.Entry.objects.using('transfer').order_by('id').all()

        for obj in qs:
            an, c = core_models.Antenna.objects.get_or_create(id=obj.id)
            if c is True:
                an.entry = core_models.Entry.objects.create()
                an.video = core_models.Video.objects.create()
                an.picture = core_models.Picture.objects.create()

            mt, c = core_models.Metadata.objects.get_or_create(url=obj.url)
            if c is True:
                mt.title = obj.title
                mt.content = obj.content
                mt.seo_title = obj.seo_title
                mt.seo_content = obj.seo_content
                mt.creator = obj.creator
                mt.publisher = obj.publisher
                mt.published_at = obj.published_at
                mt.save()

            bl, c = core_models.Blog.objects.get_or_create(rss=obj.blog.rss)
            if c is True:
                bl.url = obj.blog.url
                bl.name = obj.blog.name
                #  bl.explain = obj.blog.seo_title
                bl.mediatype = obj.blog.ex_mediatype
                bl.contenttype = obj.blog.ex_adsensetype
                bl.save()

            for vid in obj.videos.all():
                try:
                    site = core_models.Site.objects.find(domain=vid.site.domain).first()
                except core_models.Site.DoesNotExist:
                    site = None

                core_models.VideoMetadata.objects.create(
                    video=an.video,
                    site=site,
                    url=vid.url,
                    embed_code=vid.code,
                    duration=vid.duration,
                    #  title=,
                    #  content=,
                )

                for url in vid.video_urls:
                    core_models.VideoMetadata.objects.create(
                        video=an.video,
                        url=url.name,
                    )

                for code in vid.video_codes:
                    core_models.VideoMetadata.objects.create(
                        video=an.video,
                        embed_code=code.name,
                    )

                for di in vid.divas.all():
                    diva = core_models.Diva.objects.filter(name=di.name).first()
                    if diva is not None:
                        an.divas.add(diva)

            for pic in obj.pictures.all():
                try:
                    toon = core_models.Toon.objects.filter(name=pic.anime.name).first()

                    if toon is not None:
                        chars = []
                        for ch in pic.characters.all():
                            char = core_models.Char.objects.filter(name=ch.name).first()
                            if char is not None:
                                chars.append(char)

                        for chh in chars:
                            toon.chars.add(chars)

                        an.toons.add(toon)
                except models.Anime.DoesNotExist:
                    pass

                for img in pic.images.all():
                    core_models.PictureThumb.objects.create(
                        assoc_id=an.picture.id,
                        name=img.name,
                        src=img.src,
                        ext=img.ext,
                        mime=img.mime,
                        width=img.width,
                        height=img.height
                    )

            for t in obj.tags.all():
                tag = core_models.Tag.objects.filter(name=t.name).first()
                if tag is not None:
                    an.tags.add(tag)

            for img in obj.images.all():
                core_models.EntryThumb.objects.create(
                    assoc_id=an.entry.id,
                    name=img.name,
                    src=img.src,
                    ext=img.ext,
                    mime=img.mime,
                    width=img.width,
                    height=img.height
                )

            an.blog = bl
            an.metadata = mt
            an.save()
