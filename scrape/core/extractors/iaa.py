from django.core.cache import caches
from django.utils.html import strip_tags


from . import base

any_cache = caches['tmp_anything']


class Video(base.ExtractBase):

    def info(self):
        return dict(
            author=self.author(),
            title=self.title(),
            explain=self.explain(),
            comments=self.comments(),
            categories=self.categories(),
            urls=self.urls(),
            embed_codes=self.embed_codes(),
        )

    def author(self):
        sel = '.node-info .submitted a.username'

        return self.doc(sel).html()

    def title(self):
        sel = 'h1'

        return strip_tags(self.doc(sel).html())

    def explain(self):
        sel = '.field-name-body .field-item.even'

        return strip_tags(self.doc(sel).html())

    def comments(self):
        sel = '.field-name-comment-body .field-item.even'

        comments = []
        for item in self.doc(sel).items():
            comments.append(strip_tags(item.html()))
        return comments

    def categories(self):
        sel = '.field-name-field-categories .field-item.even a'

        categories = []
        for item in self.doc(sel).items():
            categories.append(strip_tags(item.html()))
        return categories

    def urls(self):
        return []

    def embed_codes(self):
        sel = 'video'

        return str(self.doc(sel))
