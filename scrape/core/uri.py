from urllib.parse import urlparse
from os.path import splitext, basename


def uriext(uri):
    disassembled = urlparse(uri)
    _, file_ext = splitext(basename(disassembled.path))
    return file_ext
