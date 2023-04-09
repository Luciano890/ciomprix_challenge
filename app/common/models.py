"""Common models for all apps."""
from datetime import datetime
from uuid import UUID, uuid4

from django.db import models

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    uuid: UUID = models.UUIDField(default=uuid4, editable=True)
    created_at: datetime = models.DateTimeField('Created At', auto_now_add=True, db_index=True)
    updated_at: datetime = models.DateTimeField('Updated At', auto_now=True)


    class Meta:
        abstract = True
