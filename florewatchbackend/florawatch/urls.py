"""
URL configuration for FloraWatch project.

FloraWatch Backend API - Sistema de detección de floración con IA
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import api_home

# Configurar el admin
admin.site.site_header = "FloraWatch Admin"
admin.site.site_title = "FloraWatch"
admin.site.index_title = "Panel de Administración FloraWatch"

urlpatterns = [
    # Home page
    path('', api_home, name='api_home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Authentication
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/', include('rest_framework.urls')),
    
    # API Endpoints
    path('api/plants/', include('plants.urls')),
    path('api/satellite/', include('satellite_data.urls')),
    path('api/predictions/', include('predictions.urls')),
    path('api/accounts/', include('accounts.urls')),
    
    # External APIs (Weather & Satellite)
    path('', include('api_urls')),
    
    # Health check
    path('health/', include('florawatch.health_urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
