from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def create(self, validated_data):
        passW = validated_data['password']
        user = User()
        user.username = validated_data['username']
        user.set_password(passW)
        user.save()

        return user
