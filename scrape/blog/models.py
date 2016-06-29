from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from core import models as core_models


class Blog(core_models.BaseModel):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    rss = models.CharField(max_length=255)

    mediatype = models.CharField(max_length=255)
    contenttype = models.CharField(max_length=255)

    last_modified = models.DateTimeField(blank=True, null=True)

    inserted_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=False)

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True)

    class Meta:
        db_table = 'blogs'

    #  belongs_to :user, Exantenna.User

    #  has_one :antenna, Exantenna.Antenna
    #  has_one :thumb, {"blogs_thumbs", Exantenna.Thumb}, foreign_key: :assoc_id
    #  has_one :penalty, {"blogs_penalties", Exantenna.Penalty}, foreign_key: :assoc_id

    #  has_many :scores, {"blogs_scores", Exantenna.Score}, foreign_key: :assoc_id
    #  has_many :verifiers, Exantenna.BlogVerifier
