from django.contrib.auth import get_user_model
from rest_framework import  serializers
from .models import Status, User

class UserSerializer(serializers.ModelSerializer):
    statuses = serializers.PrimaryKeyRelatedField(many=True, queryset=Status.objects.all())    

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'statuses')

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
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Status
        fields = ('id', 'message', 'state', 'date', 'owner')
