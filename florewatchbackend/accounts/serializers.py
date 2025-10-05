"""
Serializers para la aplicación Accounts
"""

from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import UserProfile, APIKey, UserActivity, Notification


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfiles de usuario"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer para claves API"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = APIKey
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer para actividades de usuario"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User de Django"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class GroupSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Group de Django"""

    users = UserSerializer(source='user_set', many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'users']
