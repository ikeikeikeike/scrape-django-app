import importlib

from core import client
from pyquery import PyQuery as pq


class ExtractorBase(object):

    name = None

    def __init__(self, url):
        self.url = url
        self._html = None

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
            name=self.extract_name(),
            urls=self.extract_urls(),
            embed_codes=self.extract_embed_codes(),
        )

    def extract_name(self):
        """ extracet name
        """
        return self.name

    def extract_urls(self):
        """ extracet url
        """
        raise NotImplementedError

    def extract_embed_codes(self):
        """ extracet embed_code
        """
        raise NotImplementedError


def import_extractor(name):
    kname = name.title().replace('-', '').replace('_', '')
    mname = 'core.video.extractors.%s' % name.replace('-', '_')

    try:
        mod = importlib.import_module(mname)
    except ImportError:
        return None

    return getattr(mod, kname)


def get_extractor(name, url):
    klass = import_extractor(name)

    return klass and klass(url)
