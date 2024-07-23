# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UserCreate, UserInfoView
from .views import LoginView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='create_user'),
    path('userinfo/', UserInfoView.as_view(), name='user_info'),
    path('login/', LoginView.as_view(), name='login'),
]