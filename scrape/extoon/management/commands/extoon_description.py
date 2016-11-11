from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db.models import Q

from core.extractors import dms

from extoon import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        where = Q(info__isnull=False, maker_id__isnull=False)
        where = where & Q(Q(content='') | Q(content__isnull=True))

        qs = models.Entry.objects.filter(where).order_by('updated_at')
        for entry in qs:
            entry.content = extract(entry.info.info or [])
            entry.updated_at = timezone.now()
            entry.save()


def extract(infos):
    for info in infos:
        detail = dms.Detail(info['URL'])

        if detail.ok and detail.description():
            return detail.description()

    return None
