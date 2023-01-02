from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser, Group, Permission

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
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organizations_managed'
    )


    def __str__(self):
        return self.name

class Team(models.Model):
    """Team model"""
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teams_created'
    )
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams_employed',
        blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teams_managed'
    )

    def __str__(self):
        return self.name

class Release(models.Model):
    """Release model."""
    name=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    team=models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Sprint(models.Model):
    """Sprint model."""
    name=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    release=models.ForeignKey(
        Release,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Invitation(models.Model):
    """Invitation model."""
    email = models.EmailField()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    invitation_code = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class EmployeeSignUp(AbstractUser):
    """Employee sign up model."""
    # email = models.EmailField(unique=True)
    # first_name = models.CharField(max_length=255, blank=False)
    # last_name = models.CharField(max_length=255, blank=False)
    # password = models.CharField(max_length=255)
    # username = models.CharField(max_length=255, unique=True)
    invitation_code = models.CharField(max_length=255, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')

    def __str__(self):
        return self.email