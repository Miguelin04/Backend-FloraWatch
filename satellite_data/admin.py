"""
Configuración del admin para la aplicación Satellite Data
"""
from django.contrib import admin
from .models import SatelliteDataSource, SatelliteDataCollection, SatelliteDataPoint, WeatherData


@admin.register(SatelliteDataSource)
class SatelliteDataSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'resolution', 'update_frequency', 'requires_api_key', 'is_active']
    list_filter = ['requires_api_key', 'is_active', 'update_frequency']
    search_fields = ['name', 'description']
    ordering = ['name']
    list_editable = ['is_active']


@admin.register(SatelliteDataCollection)
class SatelliteDataCollectionAdmin(admin.ModelAdmin):
    list_display = ['location', 'data_source', 'data_type', 'start_date', 'end_date', 'status', 'quality_score']
    list_filter = ['data_type', 'status', 'data_source', 'collection_date']
    search_fields = ['location__name', 'data_source__name']
    ordering = ['-collection_date']
    raw_id_fields = ['location', 'data_source']
    date_hierarchy = 'collection_date'


@admin.register(SatelliteDataPoint)
class SatelliteDataPointAdmin(admin.ModelAdmin):
    list_display = ['collection', 'timestamp', 'value', 'quality_flag']
    list_filter = ['quality_flag', 'timestamp']
    search_fields = ['collection__location__name']
    ordering = ['-timestamp']
    raw_id_fields = ['collection']
    date_hierarchy = 'timestamp'


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'date', 'temperature_avg', 'humidity', 'precipitation', 'data_source']
    list_filter = ['data_source', 'date']
    search_fields = ['location__name']
    ordering = ['-date']
    raw_id_fields = ['location']
    date_hierarchy = 'date'
