from rest_framework import permissions
from organization.models import Team

class HasTeamManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        team_id = request.query_params.get('team')

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return False

        return request.user == team.manager
