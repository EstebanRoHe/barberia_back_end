from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
