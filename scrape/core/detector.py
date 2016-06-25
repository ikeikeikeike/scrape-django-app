from pyquery import PyQuery as pq

from . import client


def is_wordpress(uri):
    doc = pq(client.html(uri) or None)
    if doc('link[href*="wp-content"]').length:
        return True
    return False
