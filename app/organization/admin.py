from django.contrib import admin

from .models import Organization, Team

admin.site.register(Organization)
admin.site.register(Team)