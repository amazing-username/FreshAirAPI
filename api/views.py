from django.contrib.auth import get_user_model, login as django_login, logout as django_logout
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Status
from .permissions import IsOwnerOrReadOnly
from .serializers import StatusSerializer, UserSerializer


class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        previously_logged_in = self.is_first_login(user.pk)
        django_login(user=user, request=request)

        return Response({
            'id': user.pk,
            'username': user.username,
            'token': token.key,
            'first_login' : previously_logged_in
        })

    def is_first_login(self, pk):
        user = get_user_model().objects.get(pk=pk)

        if user.last_login is None:
            return True

        return False

class Logout(ObtainAuthToken):        

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response({
            'detail': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data,
                                            context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'detail': 'Successfully Registered'
            })
        else:
            return Response({
                'detail': 'Registration failed'
            })


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('-id')
    serializer_class = UserSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class UserList(APIView):
    
    def get(self, request, format=None):
        users = get_user_model().objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('hello your request is')
        print(request.data)
        print('\n\n\n')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatusList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsOwnerOrReadOnly)

    def get(self, request, format=None):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)

    def post(self, request, format=None):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StatusDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        status = self.get_object(pk)
        serializer = StatusSerializer(status)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        status = self.get_object(pk)
        serializer = StatusSerializer(status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        status = self.get_object(pk)
        status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
