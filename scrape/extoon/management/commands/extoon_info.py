import time

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db.models import Q

from core.extractors import dms

from extoon import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = dms.Info()
        gorc = models.EntryInfo.objects.get_or_create

        where = Q(info__info__isnull=True)
        qs = models.Entry.objects.filter(where).order_by('updated_at')[:100]

        for e in qs:
            inf, _ = gorc(assoc_id=e.id)

            inf.info = api.info(e.title) or None
            if inf.info:
                inf.save()

            e.info = inf
            e.updated_at = timezone.now()
            e.save()

            time.sleep(1)
            if settings.ENVIRONMENT == 'prod':
                time.sleep(5)
