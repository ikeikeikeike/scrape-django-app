import random

from django.conf import settings
from django.core.cache import caches

import requests
import eventlet

from requests import adapters

img_cache = caches['tmp_image']
html_cache = caches['tmp_html']


def rq(headers=None):
    retries = adapters.HTTPAdapter(max_retries=40)
    ua = random.choice(list(settings.USER_AGENT.values()))

    s = requests.Session()

    s.headers['User-Agent'] = ua
    s.headers.update(headers or {})

    s.mount('http://', retries)
    s.mount('https://', retries)
    return s


def img(uri, headers=None):
    content = img_cache.get(uri)

    if not content:
        try:
            with eventlet.Timeout(10):
                r = rq(headers or {}).get(uri, verify=False)
        except (
            eventlet.timeout.Timeout,
            requests.exceptions.ConnectionError,
        ):
            return None

        if r.ok:
            content = r.content
            img_cache.set(uri, content)

    return content


def html(uri, headers=None):
    content = html_cache.get(uri)

    if not content:
        try:
            with eventlet.Timeout(10):
                r = rq(headers or {}).get(uri, verify=False)
        except (
            eventlet.timeout.Timeout,
            requests.exceptions.ConnectionError,
        ):
            return None

        if r.ok:
            content = r.content
            html_cache.set(uri, content)

    return content
