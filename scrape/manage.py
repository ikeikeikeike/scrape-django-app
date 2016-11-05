#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrape.settings")

    from django.core.management import execute_from_command_line

    from core import logging
    logger = logging.getLogger(__name__)

    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        logger.error(
            'Admin Command Error: %s', ' '.join(sys.argv),
            exc_info=sys.exc_info()
        )
        raise e
