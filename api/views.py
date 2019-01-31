from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .models import Status
from .serializers import StatusSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('-id')
    serializer_class = UserSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
