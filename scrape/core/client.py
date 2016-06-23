from django.conf import settings
from django.core.cache import caches

import requests

img_cache = caches['tmp_image']
html_cache = caches['tmp_image']

requests.adapters.DEFAULT_RETRIES = 5  # Force assign(patch)


def img(uri):
    content = img_cache.get(uri)
    if not content:
        content = _rq(uri).content
        img_cache.set(uri, content)

    return content


def html(uri):
    content = html_cache.get(uri)
    if not content:
        content = _rq(uri).content
        html_cache.set(uri, content)

    return content


def _rq(url):
    return requests.get(url, headers={
        'User-Agent': settings.USER_AGENT['firefox']
    })
