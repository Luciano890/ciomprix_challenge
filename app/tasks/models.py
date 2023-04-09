"""Tasks models"""
from datetime import datetime

from django.db import models

from common.models import BaseModel


class Task(BaseModel):
    """Task's model."""
    model_name = "Task"

    title: str = models.CharField(verbose_name="Title", max_length=50)
    description: str = models.CharField(verbose_name="Description", max_length=50)
    end_date: datetime = models.DateField(verbose_name="End date", null=True, blank=True)

    users = models.ManyToManyField('users.User', related_name='tasks')

    def __str__(self):
        return self.title
