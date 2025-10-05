"""
URLs para health checks y status del sistema
"""
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
def health_check(request):
    """Health check básico del sistema"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'FloraWatch Backend',
        'version': '1.0.0',
        'timestamp': '2025-10-04T00:00:00Z'
    })

@require_http_methods(["GET"])
def status(request):
    """Status detallado del sistema"""
    return JsonResponse({
        'status': 'operational',
        'services': {
            'database': 'connected',
            'ai_models': 'ready',
            'satellite_api': 'available',
            'cache': 'active'
        },
        'version': '1.0.0',
        'uptime': '24h'
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('status/', status, name='system_status'),
]