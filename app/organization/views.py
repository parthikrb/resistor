import random
import string

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from django.db.models import Q

from .models import Organization, Team, Release, Sprint, Invitation
from .serializers import OrganizationSerializer, TeamSerializer, ReleaseSerializer, SprintSerializer, InvitationSerializer, EmployeeSignUpSerializer
from .utils import invite_user


def generate_unique_code():
  code_length = 8
  code_characters = string.ascii_letters + string.digits
  code = ''.join(random.choices(code_characters, k=code_length))
  while Invitation.objects.filter(invitation_code=code).exists():
    code = ''.join(random.choices(code_characters, k=code_length))
  return code

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


class ReleaseView(viewsets.ModelViewSet):
    serializer_class = ReleaseSerializer
    queryset = Release.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return Release.objects.filter(team__employees = self.request.user)

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

class InvitationView(generics.CreateAPIView):
  serializer_class = InvitationSerializer

  def perform_create(self, serializer):
    email = self.request.data.get('email')
    organization = self.request.data.get('organization')
    invitation_code = generate_unique_code()

    try:
        organization = Organization.objects.get(id=organization)
    except Organization.DoesNotExist:
        raise ValidationError('Invalid organization')

    invite_user( email, organization, invitation_code=invitation_code)

    serializer.save(invitation_code=invitation_code)


class EmployeeSignUpView(generics.CreateAPIView):
    serializer_class = EmployeeSignUpSerializer

    def perform_create(self, serializer):
        invitation_code = self.request.data.get('invitation_code')
        try:
            invitation = Invitation.objects.get(invitation_code=invitation_code)
        except Invitation.DoesNotExist:
            raise ValidationError('Invalid invitation code')

        serializer.save()