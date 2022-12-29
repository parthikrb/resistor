from django.contrib import admin

from .models import Organization, Team, Sprint

admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(Sprint)