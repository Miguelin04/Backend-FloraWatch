
#Servicio para integración con OpenWeatherMap API proporciona datos meteorológicos para correlación con eventos de floración

import requests
import os
from django.conf import settings
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """Servicio para obtener datos meteorológicos de OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY no está configurada en las variables de entorno")
        
     # Obtiene pronóstico del clima para los próximos días
    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict]:
   
        url = f"{self.base_url}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Celsius
            'lang': 'es'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error obteniendo clima actual: {e}")
            return None
    
     # Obtiene pronóstico del clima para los próximos días
    def get_weather_forecast(self, lat: float, lon: float, days: int = 5) -> Optional[Dict]:
        url = f"{self.base_url}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'es',
            'cnt': days * 8  # 8 mediciones por día (cada 3 horas)
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error obteniendo pronóstico: {e}")
            return None
    # Obtiene pronóstico del clima para los próximos día
    def get_historical_weather(self, lat: float, lon: float) -> List[Dict]:
        logger.warning(f"API histórica requiere suscripción de pago. Ubicación: {lat},{lon}. Usando datos limitados.")
        return []
    
    def analyze_flowering_conditions(self, lat: float, lon: float) -> Dict:
       # Analiza las condiciones meteorológicas favorables para la floración
        current_weather = self.get_current_weather(lat, lon)
        forecast = self.get_weather_forecast(lat, lon)
        
        if not current_weather or not forecast:
            return {"error": "No se pudieron obtener datos meteorológicos"}
        analysis = {
            "location": {
                "lat": lat,
                "lon": lon,
                "city": current_weather.get('name', 'Desconocido')
            },
            "current_conditions": {
                "temperature": current_weather['main']['temp'],
                "humidity": current_weather['main']['humidity'],
                "pressure": current_weather['main']['pressure'],
                "description": current_weather['weather'][0]['description']
            },
            "flowering_analysis": self._evaluate_flowering_conditions(current_weather, forecast)
        }
        
        return analysis
    
    def _evaluate_flowering_conditions(self, current: Dict, forecast: Dict) -> Dict:
        """
        Evalúa si las condiciones son favorables para la floración
        """
        temp = current['main']['temp']
        humidity = current['main']['humidity']
        
        # Condiciones ideales generales para floración (pueden variar por especie)
        ideal_temp_range = (15, 25)  # °C
        ideal_humidity_range = (40, 70)  # %
        
        conditions = {
            "temperature_favorable": ideal_temp_range[0] <= temp <= ideal_temp_range[1],
            "humidity_favorable": ideal_humidity_range[0] <= humidity <= ideal_humidity_range[1],
            "precipitation_forecast": self._analyze_precipitation(forecast),
            "overall_score": 0
        }
        
        # Calcular puntuación general
        score = 0
        if conditions["temperature_favorable"]:
            score += 40
        if conditions["humidity_favorable"]:
            score += 30
        if not conditions["precipitation_forecast"]["heavy_rain_expected"]:
            score += 30
        
        conditions["overall_score"] = score
        conditions["recommendation"] = self._get_flowering_recommendation(score)
        
        return conditions
    
    def _analyze_precipitation(self, forecast: Dict) -> Dict:
        # Analiza la precipitación en el pronóstico 
        heavy_rain_threshold = 10  # mm en 3 horas
        rain_days = 0
        total_precipitation = 0
        
        for item in forecast.get('list', [])[:16]:  # Próximas 48 horas
            if 'rain' in item:
                rain_3h = item['rain'].get('3h', 0)
                total_precipitation += rain_3h
                if rain_3h > heavy_rain_threshold:
                    rain_days += 1
        
        return {
            "heavy_rain_expected": rain_days > 0,
            "total_precipitation_48h": total_precipitation,
            "rainy_periods": rain_days
        }
      # Obtiene recomendación basada en la puntuación
    def _get_flowering_recommendation(self, score: int) -> str:
      
        if score >= 80:
            return "Condiciones excelentes para floración"
        elif score >= 60:
            return "Condiciones buenas para floración"
        elif score >= 40:
            return "Condiciones moderadas para floración"
        else:
            return "Condiciones desfavorables para floración"


# Instancia global del servicio
weather_service = WeatherService() if os.getenv('OPENWEATHERMAP_API_KEY') else None