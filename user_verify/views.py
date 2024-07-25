
import time
import logging

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer

logger = logging.getLogger('myapp')

class UserCreate(APIView):
    """
    user register with unregistered username and restricted password
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Create a new user.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username for the new user (3-32 characters).',
                    minLength=3,
                    maxLength=32,
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Password for the new user (8-32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number).',
                    minLength=8,
                    maxLength=32,
                ),
            },
            required=['username', 'password'],
        ),
        responses={
            201: "Created",
            400: "Bad Request",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            success = True
            user = serializer.save()
            return Response({"success": success, "reason": ""}, status=status.HTTP_201_CREATED)
        else:
            success = False
            error_messages = extract_error_messages(serializer.errors)
            return Response({"success": success, "reason": error_messages}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Login with username & password to obtain JWT tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={
            200: "OK",
            401: "UNAUTHORIZED",
            429: "TOO MANY REQUESTS",
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        cache_key = f'failed_login_{username}'
        failed_attempts = cache.get(cache_key, 0)

        if failed_attempts >= 5:
            return Response(
                {
                    'success': False,
                    'reason': "Too many failed login attempts. Please wait a minute before trying again.",
                }, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        user = authenticate(request, username=username, password=password)
        
        if user:
            # Reset the failed attempts count on successful login
            cache.delete(cache_key)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'success': True,
                    'reason': "",
                    'access': str(refresh.access_token),
                }, 
                status=status.HTTP_200_OK,
            )
        else:
            failed_attempts += 1  
            # Set the cache to expire after 1 minute
            cache.set(cache_key, failed_attempts, timeout=60)
            return Response(
                {
                    'success': False,
                    'reason': 'Invalid credentials',
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )

def extract_error_messages(errors):
    """
    Extract error messages from serializer errors and convert to a single string.
    """
    error_messages = []
    for field, field_errors in errors.items():
        for error in field_errors:
            error_messages.append(f"{field}: {str(error)}")
    return " AND ".join(error_messages)