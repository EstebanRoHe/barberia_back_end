from rest_framework import serializers
from users.serializer import UserSerializer
from .models import Bloc
from users.models import CustomUser

class BlocSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all())
    user_details = UserSerializer(source='user', read_only=True)
    class Meta:
        model = Bloc
        fields = ['id', 'description', 'url', 'user','user_details']
       
