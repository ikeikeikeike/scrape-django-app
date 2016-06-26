import re
from urllib.parse import urlparse
from os.path import splitext, basename


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
