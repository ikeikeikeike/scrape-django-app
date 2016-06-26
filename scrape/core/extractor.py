import re
from urllib.parse import urlparse
from os.path import splitext, basename

from django.utils.html import strip_tags


def uriext(uri):
    disassembled = urlparse(uri)
    _, file_ext = splitext(basename(disassembled.path))
    return file_ext


def domain(uri):
    u = urlparse(uri)

    if "livedoor.jp" in u.netloc:
        return u.path.split('/')[1]
    elif "fc2.com" in u.netloc:
        return u.netloc.split('.')[0]
    elif "blog.jp" in u.netloc:
        return u.netloc.split('.')[0]
    elif "dip.jp" in u.netloc:
        return u.netloc.split('.')[0]
    else:
        return None


def remove_link(text):
    return re.sub(r"h?ttps?\S+", "", text)


def safe_content(text):
    return remove_link(strip_tags(text)).strip()


def safe_element(feed, *attrs):
    try:
        for attr in attrs:
            feed = feed[attr]
    except KeyError:
        return

    if isinstance(feed, str):
        return strip_tags(feed)

    return feed
