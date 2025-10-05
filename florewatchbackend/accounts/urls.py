"""
URLs para la aplicación Accounts
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import GroupListView
from . import dashboard_views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='profiles')
router.register(r'api-keys', views.APIKeyViewSet, basename='api-keys')
router.register(r'activities', views.UserActivityViewSet, basename='activities')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints de autenticación y usuario
    path('register/', 
         views.RegisterView.as_view(), 
         name='register'),
    path('profile/', 
         views.CurrentUserProfileView.as_view(), 
         name='current-profile'),
    path('change-password/', 
         views.ChangePasswordView.as_view(), 
         name='change-password'),
    path('generate-api-key/', 
         views.GenerateAPIKeyView.as_view(), 
         name='generate-api-key'),
    path('notifications/mark-read/', 
         views.MarkNotificationsReadView.as_view(), 
         name='mark-notifications-read'),
    # Dashboards personalizados
    path('dashboard/', 
         dashboard_views.user_dashboard, 
         name='user-dashboard'),
    path('dashboard/student/', 
         dashboard_views.student_dashboard, 
         name='student_dashboard'),
    path('dashboard/botanist/', 
         dashboard_views.botanist_dashboard, 
         name='botanist_dashboard'),
    path('dashboard/researcher/', 
         dashboard_views.researcher_dashboard, 
         name='researcher_dashboard'),
    path('dashboard/farmer/', 
         dashboard_views.farmer_dashboard, 
         name='farmer_dashboard'),
    path('dashboard/hobbyist/', 
         dashboard_views.hobbyist_dashboard, 
         name='hobbyist_dashboard'),
    
    # API de login personalizado
    path('login/', 
         dashboard_views.custom_login, 
         name='custom-login'),
    path('dashboard-api/', 
         dashboard_views.user_dashboard_api, 
         name='dashboard-api'),
         
    path('groups/', GroupListView.as_view(), name='group-list'),
]