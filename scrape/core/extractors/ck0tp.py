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
        sel = 'h1'

        return self.doc(sel).html()

    def urls(self):
        return []

    def embed_codes(self):
        sel, sele = '.player', 'object,iframe'

        codes = []
        for doc in self.doc(sel).items():
            d = doc(sele)
            d.remove_attr('id')
            d.children().remove_attr('id')

            codes.append(str(d))

        return codes
