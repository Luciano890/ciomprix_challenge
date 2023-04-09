"""User model."""
from django.db import models

from common.models import BaseModel

class User(BaseModel):
    """User's model."""
    model_name = "User"

    name: str = models.CharField(verbose_name="Name", max_length=50)
    document: str = models.CharField(verbose_name="Document", max_length=50, unique=True)

    def __str__(self):
        return self.name
