"""freshairapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api import views


#router = routers.DefaultRouter()
#router.register('users', views.UserViewSet)
#router.register('status', views.StatusViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]
