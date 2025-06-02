from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import *
from django.views.generic import *
from django.contrib.auth.forms import *
from django.contrib.auth import logout
from django.contrib.auth.mixins import *
from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from user.models import *
from user.serializers import *

class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class Login(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id':user.id})
        return Response({'error': 'Invalid credentials'}, status=400)
    
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            token = Token.objects.get(key=request.auth.key)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)