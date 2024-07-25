# accounts/serializers.py

import logging
import re

from django.contrib.auth.models import User
from rest_framework import serializers

logger = logging.getLogger('myapp')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if len(value) < 3 or len(value) > 32:
            raise serializers.ValidationError('Username must be between 3 and 32 characters.')
        return value

    def validate_password(self, value):
        if len(value) < 8 or len(value) > 32:
            raise serializers.ValidationError('Password must be between 8 and 32 characters.')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Password must contain at least one number.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

