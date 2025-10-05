
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth.models import User
from plants.models import PlantSpecies, Location, FloweringEvent
from predictions.models import AIModel
from satellite_data.models import SatelliteDataSource


@require_http_methods(["GET"])
def api_home(request):
    """Página de inicio del API con información del sistema"""
    
    # Estadísticas básicas
    stats = {
        'users': User.objects.count(),
        'plant_species': PlantSpecies.objects.count(),
        'locations': Location.objects.count(),
        'flowering_events': FloweringEvent.objects.count(),
        'ai_models': AIModel.objects.count(),
        'satellite_sources': SatelliteDataSource.objects.count(),
    }
    
    return JsonResponse({
        'message': '🌸 Bienvenido a FloraWatch Backend API',
        'description': 'Sistema de detección de floración con Inteligencia Artificial',
        'version': '1.0.0',
        'status': 'operational',
        'statistics': stats,
        'endpoints': {
            'admin': '/admin/',
            'authentication': {
                'token': '/api/auth/token/',
                'session': '/api/auth/'
            },
            'plants': {
                'species': '/api/plants/species/',
                'locations': '/api/plants/locations/',
                'monitors': '/api/plants/monitors/',
                'flowering_events': '/api/plants/flowering-events/',
                'statistics': '/api/plants/statistics/'
            },
            'satellite_data': {
                'sources': '/api/satellite/sources/',
                'collections': '/api/satellite/collections/',
                'data_points': '/api/satellite/data-points/',
                'weather': '/api/satellite/weather/',
                'ndvi': '/api/satellite/ndvi/{location_id}/',
                'fetch': '/api/satellite/fetch-satellite-data/'
            },
            'predictions': {
                'models': '/api/predictions/models/',
                'sessions': '/api/predictions/sessions/',
                'flowering_predictions': '/api/predictions/flowering-predictions/',
                'predict_flowering': '/api/predictions/predict/flowering/',
                'detect_current': '/api/predictions/detect/current/',
                'train_model': '/api/predictions/train-model/'
            },
            'accounts': {
                'profiles': '/api/accounts/profiles/',
                'register': '/api/accounts/register/',
                'notifications': '/api/accounts/notifications/',
                'dashboard': '/api/accounts/dashboard/'
            },
            'health': '/health/'
        },
        'documentation': {
            'admin_panel': 'http://127.0.0.1:8000/admin/',
            'api_docs': 'Utiliza herramientas como Postman o curl para probar los endpoints',
            'authentication': 'Usa /api/auth/token/ para obtener tokens de autenticación'
        },
        'contact': {
            'developer': 'Miguel Luna',
            'email': 'miguel.a.luna@unl.edu.ec',
            'organization': 'Universidad Nacional de Loja'
        }
    }, json_dumps_params={'indent': 2, 'ensure_ascii': False})