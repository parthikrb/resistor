from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Organization, Team, Sprint, Release, Invitation, EmployeeSignUp

def get_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

class SprintSerializer(serializers.ModelSerializer):
    """Sprint serializer."""

    class Meta:
        model = Sprint
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        if self.context['request'].user != self.context['team'].manager:
            raise serializers.ValidationError('You are not the manager of this team.')
        return data

    def create(self, validated_data):
        sprint = Sprint.objects.create(**validated_data)
        return sprint

class ReleaseSerializer(serializers.ModelSerializer):
    """Serializer for release model."""

    sprints = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    sprints_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Release
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        if self.context['request'].user != self.context['team'].manager:
            raise serializers.ValidationError('You are not the manager of this team.')
        return data

    def create(self, validated_data):
        release = Release.objects.create(**validated_data)
        return release

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sprints'] = [SprintSerializer(sprint).data for sprint in Sprint.objects.filter(release=instance.id)]
        return data


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = User.objects.get(id=instance.created_by.id)
        data['created_by'] = get_user(user)
        data['employees'] = [get_user(employee) for employee in instance.employees.all()]
        data['employees_count'] = instance.employees.count()

        manager = User.objects.get(id=instance.manager.id)
        data['manager'] = get_user(manager)
        return data

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'invitations']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = User.objects.get(id=instance.created_by.id)
        data['created_by'] = get_user(user)
        data['employees'] = [get_user(employee) for employee in instance.employees.all()]
        data['employees_count'] = instance.employees.count()
        data['teams_count'] = instance.teams.count()
        data['teams'] = [TeamSerializer(team).data for team in instance.teams.filter(organization=instance.id)]
        return data

class InvitationSerializer(serializers.ModelSerializer):
    """Invite user to organization serializer."""

    class Meta:
        model = Invitation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'invitation_code']

    def validate(self, data):
        organization_id = self.context['request'].data['organization']
        organization = Organization.objects.get(id=organization_id)
        if self.context['request'].user != organization.manager:
            raise serializers.ValidationError('You are not the manager of this organization.')
        return data


class EmployeeSignUpSerializer(serializers.ModelSerializer):
    """Serializer for employee sign up."""

    class Meta:
        model = EmployeeSignUp
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'invitation_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['username'] == data['email']:
            raise serializers.ValidationError('Username and email should be different.')

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists.')

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists.')

        try:
            invitation = Invitation.objects.get(invitation_code=data['invitation_code'])
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invitation code is invalid.')

        try:
            organization = Organization.objects.get(id=invitation.organization.id)
        except Organization.DoesNotExist:
            raise serializers.ValidationError('Organization does not exist.')

        if organization.employees.filter(email=data['email']).exists():
            raise serializers.ValidationError('You are already an employee of this organization.')

        if invitation.is_used:
            raise serializers.ValidationError('Invitation code is already used.')

        if invitation.email != data['email']:
            raise serializers.ValidationError('Invitation code is not for this email.')

        return data

    def create(self, validated_data):
        invitation_code = validated_data.pop('invitation_code')
        invitation = Invitation.objects.get(invitation_code=invitation_code)

        user = User.objects.create_user(**validated_data)

        organization = Organization.objects.get(id=invitation.organization.id)
        organization.employees.add(user)

        invitation.is_used = True
        invitation.save()
        return user