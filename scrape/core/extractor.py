import re
import unicodedata

from urllib.parse import urlparse
from os.path import splitext, basename

from django.utils.html import strip_tags

import regex
import dateparser

alias_ptn = re.compile(r'\(|\)|,|、|（|）')
num_ptn = re.compile(r'\d')


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


def safe_romaji(word):
    if word:
        return num_ptn.sub('', word.replace('-', '').replace('_', '').lower())
    return word


def safe_kana(word):
    if word:
        return num_ptn.sub('', word.replace('-', '').replace('_', ''))
    return word


def separate_alias(name):
    names = [w for w in alias_ptn.split(name) if w]
    if len(names) > 1:
        return names[0], names[1:]
    return names[0], []


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
