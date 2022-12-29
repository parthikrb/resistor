from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Organization, Team, Sprint

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
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        user = User.objects.get(id=instance.created_by.id)
        data['created_by'] = get_user(user)
        data['employees'] = [get_user(employee) for employee in instance.employees.all()]
        data['employees_count'] = instance.employees.count()
        data['teams_count'] = instance.teams.count()
        data['teams'] = [TeamSerializer(team).data for team in instance.teams.filter(organization=instance.id)]
        return data

