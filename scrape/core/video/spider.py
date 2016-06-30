import importlib
from urllib import parse

import tldextract

from core import client
from pyquery import PyQuery as pq


def get_host(url, path=''):
    p = parse.urlparse(url)
    return parse.urljoin('%s://%s' % (p.scheme, p.netloc), path)


class KeyListStorage(dict):
    def upsert(self, key, value):
        data = self.get(key)
        if not isinstance(value, (list, set, tuple)):
            value = [value]
        if data:
            value = data + value

        self.update({key: value})

    def query(self, query):
        return [
            self.get(key) for
            key in self.keys() if query(key)
        ]


class SpiderBase(object):

    name = None

    def __init__(self, url):
        self.url = url
        self._html = None
        self._images = KeyListStorage()

    def __repr__(self):
        return self.name

    # @property
    # def ok(self):
    #     return self.name

    @property
    def html(self):
        if self._html is None:
            self._html = client.html(self.url)
        return self._html

    @property
    def doc(self):
        return pq(self.html or None)

    def info(self):
        return dict(
            url=self.url,
            name=self.extract_name(),
            tags=self.extract_tags(),
            divas=self.extract_divas(),
            duration=self.extract_duration(),
            title=self.extract_title(),
            content=self.extract_content(),
            embed_code=self.extract_embed_code(),
            image_urls=self.extract_image_urls(),
        )

    def extract_name(self):
        return self.name

    def extract_tags(self):
        """ extracet tags
        """
        raise NotImplementedError

    def extract_divas(self):
        """ extracet divas
        """
        return []

    def extract_duration(self):
        """ extracet duration
        """
        raise NotImplementedError

    def extract_title(self):
        """ extracet title
        """
        raise NotImplementedError

    def extract_content(self):
        """ extracet content
        """
        raise NotImplementedError

    def extract_embed_code(self):
        """ extracet embed_code
        """
        raise NotImplementedError

    def extract_image_urls(self):
        """ extracet image_urls
        """
        raise NotImplementedError


def spider(url):
    name = tldextract.extract(url).domain

    mod_name = 'core.video.spiders.%s' % name.replace('-', '_')
    mod = importlib.import_module(mod_name)

    klass_name = name.title().replace('-', '')
    klass = getattr(mod, klass_name)

    return klass(url)
