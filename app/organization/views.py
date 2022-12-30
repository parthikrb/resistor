from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q

from .models import Organization, Team, Sprint
from .serializers import OrganizationSerializer, TeamSerializer, SprintSerializer

class OrganizationView(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(created_by=self.request.user or self.request.user in self.queryset.employees.all())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TeamView(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        return Team.objects.filter(
            Q(employees = self.request.user) | Q(manager = self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SprintView(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    queryset = Sprint.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return Sprint.objects.filter(team__employees = self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)