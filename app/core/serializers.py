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