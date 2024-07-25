# myapp/urls.py
from django.urls import path, include
from .views import UserCreate
from .views import LoginView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
]