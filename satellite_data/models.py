"""
Modelos para la aplicación Satellite Data
Gestiona datos satelitales de NASA y otras fuentes
"""

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.geos import Polygon, Point
from plants.models import Location
import json


class SatelliteDataSource(models.Model):
    """Fuentes de datos satelitales disponibles"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    api_endpoint = models.URLField(verbose_name="Endpoint API")
    
    # Configuración
    requires_api_key = models.BooleanField(default=False, verbose_name="Requiere API Key")
    update_frequency = models.CharField(
        max_length=50,
        help_text="Frecuencia de actualización (ej: daily, weekly)",
        verbose_name="Frecuencia de actualización"
    )
    resolution = models.CharField(
        max_length=50,
        help_text="Resolución espacial (ej: 250m, 1km)",
        verbose_name="Resolución"
    )
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Fuente de datos satelital"
        verbose_name_plural = "Fuentes de datos satelitales"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SatelliteDataCollection(models.Model):
    """Colección de datos satelitales para una ubicación y período"""
    
    DATA_TYPES = [
        ('ndvi', 'NDVI - Índice de Vegetación'),
        ('evi', 'EVI - Índice de Vegetación Mejorado'),
        ('lst', 'LST - Temperatura de Superficie'),
        ('precipitation', 'Precipitación'),
        ('temperature', 'Temperatura'),
        ('modis_phenology', 'MODIS Fenología'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Ubicación")
    data_source = models.ForeignKey(SatelliteDataSource, on_delete=models.CASCADE, verbose_name="Fuente")
    
    # Información de la recolección
    data_type = models.CharField(max_length=50, choices=DATA_TYPES, verbose_name="Tipo de datos")
    collection_date = models.DateField(verbose_name="Fecha de recolección")
    start_date = models.DateField(verbose_name="Fecha inicio datos")
    end_date = models.DateField(verbose_name="Fecha fin datos")
    
    # Metadatos
    quality_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Calidad de los datos (0-1)",
        verbose_name="Calidad"
    )
    cloud_coverage = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Cobertura de nubes (%)",
        verbose_name="Cobertura nubes (%)"
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('processing', 'Procesando'),
            ('completed', 'Completado'),
            ('error', 'Error'),
        ],
        default='pending',
        verbose_name="Estado"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Colección de datos satelital"
        verbose_name_plural = "Colecciones de datos satelitales"
        ordering = ['-collection_date']
        unique_together = ['location', 'data_source', 'data_type', 'start_date', 'end_date']
    
    def __str__(self):
        return f"{self.location.name} - {self.data_type} ({self.start_date} to {self.end_date})"


class SatelliteDataPoint(models.Model):
    """Punto individual de datos satelitales"""
    
    collection = models.ForeignKey(
        SatelliteDataCollection, 
        on_delete=models.CASCADE, 
        related_name='data_points',
        verbose_name="Colección"
    )
    
    # Datos temporales
    timestamp = models.DateTimeField(verbose_name="Fecha y hora")
    
    # Valores de datos
    value = models.FloatField(verbose_name="Valor principal")
    quality_flag = models.CharField(
        max_length=20,
        choices=[
            ('good', 'Buena'),
            ('fair', 'Regular'),
            ('poor', 'Pobre'),
            ('bad', 'Mala'),
        ],
        default='good',
        verbose_name="Calidad"
    )
    
    # Datos adicionales (JSON flexible)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Metadatos adicionales en formato JSON",
        verbose_name="Metadatos"
    )
    
    # Coordenadas geoespaciales
    coordinates = models.PointField(
        null=True,
        blank=True,
        verbose_name="Coordenadas específicas",
        help_text="Punto geográfico específico si difiere de la ubicación principal"
    )
    
    # Coordenadas tradicionales (para compatibilidad)
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="Latitud específica"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name="Longitud específica"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Punto de datos satelital"
        verbose_name_plural = "Puntos de datos satelitales"
        ordering = ['-timestamp']
        unique_together = ['collection', 'timestamp']
    
    def __str__(self):
        return f"{self.collection.data_type}: {self.value} ({self.timestamp.date()})"


class WeatherData(models.Model):
    """Datos meteorológicos complementarios"""
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Ubicación")
    
    # Datos temporales
    date = models.DateField(verbose_name="Fecha")
    
    # Datos meteorológicos
    temperature_min = models.FloatField(null=True, blank=True, verbose_name="Temp. mínima (°C)")
    temperature_max = models.FloatField(null=True, blank=True, verbose_name="Temp. máxima (°C)")
    temperature_avg = models.FloatField(null=True, blank=True, verbose_name="Temp. promedio (°C)")
    
    humidity = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Humedad (%)"
    )
    
    precipitation = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Precipitación (mm)"
    )
    
    wind_speed = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Velocidad viento (km/h)"
    )
    
    wind_direction = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
        verbose_name="Dirección viento (°)"
    )
    
    pressure = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(800), MaxValueValidator(1200)],
        verbose_name="Presión (hPa)"
    )
    
    # Fuente de datos
    data_source = models.CharField(
        max_length=100,
        default='api',
        verbose_name="Fuente de datos"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Datos meteorológicos"
        verbose_name_plural = "Datos meteorológicos"
        ordering = ['-date']
        unique_together = ['location', 'date']
    
    def __str__(self):
        return f"{self.location.name} - {self.date}"
