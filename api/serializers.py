from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Status, User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.save()

        return user

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('message', 'state', 'date', 'user')
