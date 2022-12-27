from django.db import models
from django.conf import settings

class Organization(models.Model):
    """Organization model"""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organizations_created'
    )
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='organizations_employed',
        blank=True
    )


    def __str__(self):
        return self.name