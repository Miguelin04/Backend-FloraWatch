"""
Views para la aplicación Accounts
"""

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile, APIKey, UserActivity, Notification
from .serializers import (
    UserProfileSerializer, APIKeySerializer, UserActivitySerializer, NotificationSerializer
)
from django.contrib.auth.models import Group
from rest_framework import generics
from .serializers import GroupSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet para perfiles de usuario"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    """ViewSet para claves API"""
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer


class UserActivityViewSet(viewsets.ModelViewSet):
    """ViewSet para actividades de usuario"""
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet para notificaciones"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class RegisterView(APIView):
    """Vista para registro de usuarios"""
    
    def post(self, request):
        return Response({"message": "Registro de usuario - En desarrollo"})


class CurrentUserProfileView(APIView):
    """Vista para perfil de usuario actual"""
    
    def get(self, request):
        return Response({"message": "Perfil actual - En desarrollo"})


class ChangePasswordView(APIView):
    """Vista para cambiar contraseña"""
    
    def post(self, request):
        return Response({"message": "Cambiar contraseña - En desarrollo"})


class GenerateAPIKeyView(APIView):
    """Vista para generar clave API"""
    
    def post(self, request):
        return Response({"message": "Generar API key - En desarrollo"})


class MarkNotificationsReadView(APIView):
    """Vista para marcar notificaciones como leídas"""
    
    def post(self, request):
        return Response({"message": "Marcar notificaciones - En desarrollo"})


class UserDashboardView(APIView):
    """Vista para dashboard de usuario"""
    
    def get(self, request):
        return Response({"message": "Dashboard de usuario - En desarrollo"})


class GroupListView(generics.ListAPIView):
    """Vista para listar grupos y sus usuarios"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
