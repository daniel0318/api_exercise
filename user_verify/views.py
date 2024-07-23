from django.shortcuts import render

# Create your views here.
# Create your views here.
# accounts/views.py

import time
import sys
import json

# from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
# from django.urls import path
# from django.db import connection
# from django.http import HttpResponse

from rest_framework.permissions import AllowAny
from rest_framework import generics
# from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from rest_framework import generics, mixins, viewsets

from .serializers import UserSerializer

from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.conf import settings
import time

class UserCreate(generics.CreateAPIView):
    """
    Create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Create a new user.",
        responses={201: UserSerializer, 400: "Bad Request"}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            'fullname': user.get_full_name(),
        }
        return Response(data)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f'failed_login_{username}'
        failed_attempts = cache.get(cache_key, 0)

        if failed_attempts >= 5:
            return Response({'error': 'Too many failed login attempts. Please wait a minute before trying again.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            cache.delete(cache_key)  # Reset the failed attempts count on successful login
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            failed_attempts += 1
            cache.set(cache_key, failed_attempts, timeout=60)  # Set the cache to expire after 1 minute
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)# 