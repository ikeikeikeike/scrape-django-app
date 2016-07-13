import random

from django.conf import settings
from django.core.cache import caches

import requests
import eventlet

from requests import adapters

img_cache = caches['tmp_image']
any_cache = caches['tmp_anything']


def rq(headers=None):
    retries = adapters.HTTPAdapter(max_retries=40)
    ua = random.choice(list(settings.USER_AGENT.values()))

    s = requests.Session()

    s.headers['User-Agent'] = ua
    s.headers.update(headers or {})

    s.mount('http://', retries)
    s.mount('https://', retries)
    return s


def img(uri, headers=None, auth=None):
    content = img_cache.get(uri)

    if not content:
        r = cached_request(uri, headers, auth)
        if r and r.ok:
            content = r.content
            img_cache.set(uri, content)

    return content


def json(uri, headers=None, auth=None):
    js = any_cache.get(uri)

    if not js:
        r = cached_request(uri, headers, auth)
        if r and r.ok:
            js = r.json()
            any_cache.set(uri, js)

    return js


def html(uri, headers=None, auth=None):
    content = any_cache.get(uri)

    if not content:
        r = cached_request(uri, headers, auth)
        if r and r.ok:
            content = r.content
            any_cache.set(uri, content)

    return content


def cached_request(uri, headers=None, auth=None):
    try:
        with eventlet.Timeout(10):
            r = rq(headers or {}).get(uri, verify=False, auth=auth)
    except (
        eventlet.timeout.Timeout,
        requests.exceptions.ConnectionError,
    ):
        return None
    return r
