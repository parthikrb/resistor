from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User with this username already exists')
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = instance.email
        data['teams_managing'] = [team.id for team in instance.teams_managed.all()]
        data['teams_managing_count'] = instance.teams_managed.count()
        data['teams_employing'] = [team.id for team in instance.teams_employed.all()]
        data['teams_employing_count'] = instance.teams_employed.count()
        data['organizations_managing'] = [organization.id for organization in instance.organizations_managed.all()]
        data['organizations_managing_count'] = instance.organizations_managed.count()
        return data
