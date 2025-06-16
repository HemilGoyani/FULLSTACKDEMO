from django.db import models

from backend.models import BaseModel


class Settings(BaseModel):
    terms_and_conditions = models.TextField(blank=True, null=True)
    scope_of_works = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
