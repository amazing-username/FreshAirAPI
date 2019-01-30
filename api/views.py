from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('-id')
    serializer_class = UserSerializer
