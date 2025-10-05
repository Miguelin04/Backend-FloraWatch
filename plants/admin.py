"""
Configuración del admin para la aplicación Plants
"""
from django.contrib import admin
from .models import PlantSpecies, Location, PlantMonitor, FloweringEvent


@admin.register(PlantSpecies)
class PlantSpeciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'plant_type', 'is_active', 'created_at']
    list_filter = ['plant_type', 'is_active', 'created_at']
    search_fields = ['name', 'scientific_name']
    ordering = ['name']
    list_editable = ['is_active']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'country', 'region', 'is_active']
    list_filter = ['country', 'region', 'is_active']
    search_fields = ['name', 'country', 'region']
    ordering = ['name']
    list_editable = ['is_active']


@admin.register(PlantMonitor)
class PlantMonitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'identifier', 'species', 'location', 'is_monitored', 'created_by']
    list_filter = ['species', 'location', 'is_monitored', 'monitoring_start_date']
    search_fields = ['name', 'identifier', 'species__name', 'location__name']
    ordering = ['name']
    list_editable = ['is_monitored']
    raw_id_fields = ['species', 'location', 'created_by']


@admin.register(FloweringEvent)
class FloweringEventAdmin(admin.ModelAdmin):
    list_display = ['plant_monitor', 'flowering_stage', 'detection_method', 'confidence_score', 'detection_date']
    list_filter = ['flowering_stage', 'detection_method', 'detection_date']
    search_fields = ['plant_monitor__name', 'plant_monitor__identifier']
    ordering = ['-detection_date']
    raw_id_fields = ['plant_monitor', 'reported_by']
    date_hierarchy = 'detection_date'
