"""
Serializers para la aplicación Plants
"""

from rest_framework import serializers
from .models import PlantSpecies, Location, PlantMonitor, FloweringEvent


class PlantSpeciesSerializer(serializers.ModelSerializer):
    """Serializer para especies de plantas"""
    
    class Meta:
        model = PlantSpecies
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    """Serializer para ubicaciones"""
    
    class Meta:
        model = Location
        fields = '__all__'


class PlantMonitorSerializer(serializers.ModelSerializer):
    """Serializer para monitores de plantas"""
    
    species_name = serializers.CharField(source='species.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = PlantMonitor
        fields = '__all__'


class FloweringEventSerializer(serializers.ModelSerializer):
    """Serializer para eventos de floración"""
    
    plant_name = serializers.CharField(source='plant_monitor.name', read_only=True)
    species_name = serializers.CharField(source='plant_monitor.species.name', read_only=True)
    
    class Meta:
        model = FloweringEvent
        fields = '__all__'