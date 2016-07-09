from __future__ import unicode_literals

from django.db import models

from core import models as core_models


class Blog(core_models.BaseModel):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rss = models.CharField(max_length=255)

    mediatype = models.CharField(max_length=255)
    contenttype = models.CharField(max_length=255)

    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'blogs'
