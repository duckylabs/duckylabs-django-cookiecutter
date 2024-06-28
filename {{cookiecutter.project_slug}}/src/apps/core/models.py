# Create your models here.
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        _("created_at"), editable=False, auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        _("updated_at"), editable=False, auto_now=True, db_index=True
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    uuid = models.UUIDField(
        "UUID", editable=False, unique=True, db_index=True, default=uuid.uuid4
    )

    class Meta:
        abstract = True


class UUIDTimeStampedModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True
