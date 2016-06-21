from django.utils.html import strip_tags


def safe(feed, *attrs):
    try:
        for attr in attrs:
            feed = getattr(feed, attr)
    except AttributeError:
        return

    if isinstance(feed, str):
        return strip_tags(feed)

    return feed
