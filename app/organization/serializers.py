from rest_framework import serializers

from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_at', 'updated_at', 'created_by', 'employees']
        read_only_fields = ['created_at', 'updated_at', 'created_by']