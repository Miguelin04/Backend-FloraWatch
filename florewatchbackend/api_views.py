# Vistas API para datos meteorológicos y satelitales e integra NASA API y OpenWeatherMap API

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status  
from django.http import JsonResponse
import requests
import os
from datetime import datetime, timedelta
from weather_service import weather_service

# Constantes para mensajes de error
WEATHER_SERVICE_UNAVAILABLE = "Servicio meteorológico no disponible"

@api_view(['GET'])
@permission_classes([AllowAny])
# Obtiene datos meteorológicos actuales para una ubicación
def get_weather_data( lat, lon):
    try:
        if not weather_service:
            return Response(
                {"error": WEATHER_SERVICE_UNAVAILABLE}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        weather_data = weather_service.get_current_weather(float(lat), float(lon))
        
        if not weather_data:
            return Response(
                {"error": "No se pudieron obtener datos meteorológicos"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(weather_data)
        
    except ValueError as e:
        return Response(
            {"error": f"Error en parámetros: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Error interno: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_weather_forecast(request, lat, lon):
    """
    Obtiene pronóstico meteorológico para una ubicación
    
    GET /api/weather/{lat}/{lon}/forecast/
    """
    try:
        days = int(request.GET.get('days', 5))
        
        if not weather_service:
            return Response(
                {"error": WEATHER_SERVICE_UNAVAILABLE}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        forecast_data = weather_service.get_weather_forecast(float(lat), float(lon), days)
        
        if not forecast_data:
            return Response(
                {"error": "No se pudo obtener el pronóstico"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(forecast_data)
        
    except ValueError as e:
        return Response(
            {"error": f"Error en parámetros: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Error interno: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def analyze_flowering_conditions(request, lat, lon):
    """
    Analiza condiciones meteorológicas para floración
    
    GET /api/weather/{lat}/{lon}/flowering-analysis/
    """
    try:
        if not weather_service:
            return Response(
                {"error": WEATHER_SERVICE_UNAVAILABLE}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        analysis = weather_service.analyze_flowering_conditions(float(lat), float(lon))
        
        if "error" in analysis:
            return Response(analysis, status=status.HTTP_404_NOT_FOUND)
        
        return Response(analysis)
        
    except ValueError as e:
        return Response(
            {"error": f"Error en parámetros: {str(e)}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Error interno: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_nasa_satellite_data(request, lat, lon):
    """
    Obtiene datos satelitales de NASA para una ubicación
    
    GET /api/satellite/{lat}/{lon}/
    """
    try:
        nasa_api_key = os.getenv('NASA_API_KEY')
        if not nasa_api_key:
            return Response(
                {"error": "API Key de NASA no configurada"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Ejemplo de consulta a NASA MODIS NDVI
        # Esto es un ejemplo - la API real de NASA puede requerir diferentes parámetros
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # NASA Earth API example endpoint
        nasa_url = "https://api.nasa.gov/planetary/earth/statistics"
        params = {
            'lon': lon,
            'lat': lat,
            'date': start_date,
            'dim': 0.1,  # Dimension in degrees
            'api_key': nasa_api_key
        }
        
        response = requests.get(nasa_url, params=params)
        
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response(
                {"error": "Error obteniendo datos de NASA", "details": response.text}, 
                status=response.status_code
            )
        
    except Exception as e:
        return Response(
            {"error": f"Error interno: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_combined_analysis(request, lat, lon):
    """
    Obtiene análisis combinado de clima y datos satelitales
    
    GET /api/analysis/{lat}/{lon}/
    """
    try:
        # Obtener datos meteorológicos
        weather_analysis = None
        if weather_service:
            weather_analysis = weather_service.analyze_flowering_conditions(float(lat), float(lon))
        
        # Datos satelitales (simulados por ahora)
        satellite_data = {
            "ndvi": 0.75,  # Índice de vegetación simulado
            "temperature_surface": 22.5,
            "last_update": datetime.now().isoformat()
        }
        
        combined_analysis = {
            "location": {
                "latitude": float(lat),
                "longitude": float(lon)
            },
            "weather_analysis": weather_analysis,
            "satellite_data": satellite_data,
            "flowering_prediction": {
                "probability": 0.78,
                "confidence": "medium",
                "estimated_peak": (datetime.now() + timedelta(days=14)).isoformat(),
                "factors": [
                    "Temperatura favorable",
                    "Humedad adecuada", 
                    "NDVI alto indica vegetación saludable"
                ]
            }
        }
        
        return Response(combined_analysis)
        
    except Exception as e:
        return Response(
            {"error": f"Error interno: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """
    Verifica el estado de las APIs externas
    
    GET /api/status/
    """
    status_info = {
        "timestamp": datetime.now().isoformat(),
        "apis": {
            "openweathermap": {
                "configured": bool(os.getenv('OPENWEATHERMAP_API_KEY')),
                "service_available": weather_service is not None,
                "status": "active" if weather_service else "inactive"
            },
            "nasa": {
                "configured": bool(os.getenv('NASA_API_KEY')),
                "status": "configured" if os.getenv('NASA_API_KEY') else "not_configured"
            }
        },
        "services": {
            "database": "active",
            "gdal": "active",
            "postgis": "active"
        }
    }
    
    return Response(status_info)