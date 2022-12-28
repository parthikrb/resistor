from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Organization, Team
from .serializers import OrganizationSerializer, TeamSerializer

class OrganizationView(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user or self.request.user in self.queryset.employees.all())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TeamView(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user or self.request.user in self.queryset.employees.all())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)