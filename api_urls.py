# URLs para las APIs de clima y datos satelitales
from django.urls import path
import api_views

urlpatterns = [
    # Estado de APIs
    path('api/status/', api_views.api_status, name='api_status'),
    
    # APIs meteorológicas
    path('api/weather/<str:lat>/<str:lon>/', api_views.get_weather_data, name='weather_current'),
    path('api/weather/<str:lat>/<str:lon>/forecast/', api_views.get_weather_forecast, name='weather_forecast'),
    path('api/weather/<str:lat>/<str:lon>/flowering-analysis/', api_views.analyze_flowering_conditions, name='flowering_analysis'),
    
    # APIs satelitales
    path('api/satellite/<str:lat>/<str:lon>/', api_views.get_nasa_satellite_data, name='satellite_data'),
    
    # Análisis combinado
    path('api/analysis/<str:lat>/<str:lon>/', api_views.get_combined_analysis, name='combined_analysis'),
]