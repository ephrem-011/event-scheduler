from django.urls import path
from user import views
from django.contrib.auth.views import *

urlpatterns = [
    
    path('api/register', views.Register.as_view(), name='register'),
    path('api/login', views.Login.as_view(), name='login'),
    path('api/logout', views.Logout.as_view(), name='logout')
    
]