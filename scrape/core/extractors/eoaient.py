from django.core.cache import caches

from . import base

any_cache = caches['tmp_anything']


class Video(base.ExtractBase):

    def info(self):
        return dict(
            title=self.title(),
            urls=self.urls(),
            embed_codes=self.embed_codes(),
        )

    def title(self):
        sel = '#page_headline'

        return self.doc(sel).html()

    def urls(self):
        sel = '.data-link li a'

        urls = []
        for doc in self.doc(sel).items():
            urls.append(doc.html())
        return urls

    def embed_codes(self):
        sel, sele = '.accordion .video-container', 'object,iframe'

        codes = []
        for doc in self.doc(sel).items():
            codes.append(str(doc(sele)))
        return codes
