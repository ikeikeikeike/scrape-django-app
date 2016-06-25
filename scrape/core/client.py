import random

from django.conf import settings
from django.core.cache import caches

import requests
from requests.adapters import HTTPAdapter

img_cache = caches['tmp_image']
html_cache = caches['tmp_html']


def rq():
    retries = HTTPAdapter(max_retries=5)
    ua = random.choice(list(settings.USER_AGENT.values()))

    s = requests.Session()
    s.headers['User-Agent'] = ua
    s.mount('http://', retries)
    s.mount('https://', retries)
    return s


def img(uri):
    content = img_cache.get(uri)

    if not content:
        try:
            r = rq().get(uri)
        except requests.exceptions.ConnectionError:
            return None

        if r.ok:
            content = r.content
            img_cache.set(uri, content)

    return content


def html(uri):
    content = html_cache.get(uri)

    if not content:
        try:
            r = rq().get(uri)
        except requests.exceptions.ConnectionError:
            return None

        if r.ok:
            content = r.content
            html_cache.set(uri, content)

    return content
