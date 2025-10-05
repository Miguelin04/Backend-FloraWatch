"""
Serializers para la aplicación Satellite Data
"""

from rest_framework import serializers
from .models import SatelliteDataSource, SatelliteDataCollection, SatelliteDataPoint, WeatherData


class SatelliteDataSourceSerializer(serializers.ModelSerializer):
    """Serializer para fuentes de datos satelitales"""
    
    class Meta:
        model = SatelliteDataSource
        fields = '__all__'


class SatelliteDataCollectionSerializer(serializers.ModelSerializer):
    """Serializer para colecciones de datos satelitales"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    source_name = serializers.CharField(source='data_source.name', read_only=True)
    
    class Meta:
        model = SatelliteDataCollection
        fields = '__all__'


class SatelliteDataPointSerializer(serializers.ModelSerializer):
    """Serializer para puntos de datos satelitales"""
    
    collection_info = serializers.CharField(source='collection.data_type', read_only=True)
    
    class Meta:
        model = SatelliteDataPoint
        fields = '__all__'


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer para datos meteorológicos"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = '__all__'