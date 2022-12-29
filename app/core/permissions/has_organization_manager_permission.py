from rest_framework import permissions
from organization.models import Organization

class HasOrganizationManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        organization_id = request.query_params.get('organization')

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return False

        return request.user == organization.manager