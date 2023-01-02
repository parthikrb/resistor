from django.contrib import admin

from .models import Organization, Team, Release,Sprint, Invitation

admin.site.register(Organization)
admin.site.register(Team)
admin.site.register(Release)
admin.site.register(Sprint)
admin.site.register(Invitation)