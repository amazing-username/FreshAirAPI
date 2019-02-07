from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('user/status/', views.StatusList.as_view()),
    path('user/status/<int:pk>/', views.StatusDetail.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/user/', views.Register.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
