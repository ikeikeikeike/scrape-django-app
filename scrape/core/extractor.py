import re
import unicodedata

from urllib.parse import urlparse
from os.path import splitext, basename

from django.utils.html import strip_tags

import regex
import dateparser


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


def find_date(orig):
    s = unicodedata.normalize('NFKC', orig)
    s = "".join(s.split())
    s = regex.sub(r'\d{1,2}歳', '', s)

    try:
        for _ in s:
            date = dateparser.parse(s)
            if date:
                return date

            s = _remove_right(s)

        for _ in s:
            date = dateparser.parse(s)
            if date:
                return date

            s = _remove_left(s)

    except ValueError:
        pass

    return None


def _remove_right(letters):
    length = len(letters)
    letter = letters[length - 1]

    if letter == u"日":
        return letters
    try:
        int(letter)
        return letters
    except ValueError:
        pass

    return letters[:length - 1]


def _remove_left(letters):
    letter = letters[0]

    try:
        int(letter)
        return letters
    except ValueError:
        pass

    return letters[1::]
