from django.utils.html import strip_tags


def safe(feed, *attrs):
    try:
        for attr in attrs:
            feed = feed[attr]
    except KeyError:
        return

    if isinstance(feed, str):
        return strip_tags(feed)

    return feed
