"""
Modelos para la aplicación Plants
Gestiona información de plantas y especies monitoreadas
"""

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.gis.geos import Point


class PlantSpecies(models.Model):
    """Especies de plantas que monitoreamos"""
    
    PLANT_TYPES = [
        ('tree', 'Árbol'),
        ('shrub', 'Arbusto'),
        ('flower', 'Flor'),
        ('crop', 'Cultivo'),
        ('grass', 'Pasto'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nombre común")
    scientific_name = models.CharField(max_length=300, verbose_name="Nombre científico", unique=True)
    plant_type = models.CharField(max_length=20, choices=PLANT_TYPES, verbose_name="Tipo de planta")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    # Información de floración
    typical_flowering_months = models.CharField(
        max_length=100, 
        help_text="Meses típicos de floración (ej: Marzo-Mayo)",
        verbose_name="Meses de floración"
    )
    flowering_duration = models.PositiveIntegerField(
        default=30,
        help_text="Duración típica de floración en días",
        verbose_name="Duración floración (días)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    
    class Meta:
        verbose_name = "Especie de planta"
        verbose_name_plural = "Especies de plantas"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.scientific_name})"


class Location(models.Model):
    """Ubicaciones geográficas donde monitoreamos plantas"""
    
    name = models.CharField(max_length=200, verbose_name="Nombre del lugar")
    
    # Campo geoespacial PostGIS
    coordinates = models.PointField(
        verbose_name="Coordenadas",
        help_text="Punto geográfico (longitud, latitud) en formato WGS84",
        default=Point(0, 0)  # Punto por defecto (0, 0)
    )
    
    # Campos tradicionales mantenidos para compatibilidad
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Latitud",
        help_text="Solo lectura - se actualiza automáticamente desde coordinates"
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Longitud", 
        help_text="Solo lectura - se actualiza automáticamente desde coordinates"
    )
    altitude = models.FloatField(null=True, blank=True, verbose_name="Altitud (m)")
    
    # Información adicional
    country = models.CharField(max_length=100, verbose_name="País")
    region = models.CharField(max_length=100, blank=True, verbose_name="Región/Estado")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        """Sincronizar coordenadas PostGIS con campos tradicionales"""
        if self.coordinates:
            self.longitude = self.coordinates.x
            self.latitude = self.coordinates.y
        elif self.latitude and self.longitude:
            # Crear Point si solo tenemos lat/lng
            self.coordinates = Point(float(self.longitude), float(self.latitude))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class PlantMonitor(models.Model):
    """Instancias específicas de plantas que monitoreamos"""
    
    species = models.ForeignKey(PlantSpecies, on_delete=models.CASCADE, verbose_name="Especie")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Ubicación")
    
    # Identificación
    identifier = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Identificador único para esta planta (ej: OAK_001_MADRID)",
        verbose_name="Identificador"
    )
    name = models.CharField(
        max_length=200, 
        help_text="Nombre descriptivo (ej: Roble del Parque del Retiro)",
        verbose_name="Nombre"
    )
    
    # Estado de monitoreo
    is_monitored = models.BooleanField(default=True, verbose_name="En monitoreo")
    monitoring_start_date = models.DateField(verbose_name="Inicio monitoreo")
    monitoring_end_date = models.DateField(null=True, blank=True, verbose_name="Fin monitoreo")
    
    # Información adicional
    notes = models.TextField(blank=True, verbose_name="Notas")
    photo = models.ImageField(upload_to='plants/photos/', blank=True, verbose_name="Foto")
    
    # Usuario responsable
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Monitor de planta"
        verbose_name_plural = "Monitores de plantas"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.species.name}"


class FloweringEvent(models.Model):
    """Eventos de floración observados o detectados"""
    
    DETECTION_METHODS = [
        ('visual', 'Observación visual'),
        ('satellite', 'Detección satelital'),
        ('ai_model', 'Modelo de IA'),
        ('user_report', 'Reporte de usuario'),
    ]
    
    FLOWERING_STAGES = [
        ('bud', 'Capullo'),
        ('early', 'Floración temprana'),
        ('peak', 'Floración máxima'),
        ('late', 'Floración tardía'),
        ('end', 'Fin de floración'),
    ]
    
    plant_monitor = models.ForeignKey(PlantMonitor, on_delete=models.CASCADE, verbose_name="Planta")
    
    # Información del evento
    detection_date = models.DateTimeField(verbose_name="Fecha de detección")
    flowering_stage = models.CharField(
        max_length=20, 
        choices=FLOWERING_STAGES,
        verbose_name="Etapa de floración"
    )
    detection_method = models.CharField(
        max_length=20, 
        choices=DETECTION_METHODS,
        verbose_name="Método de detección"
    )
    
    # Confianza y datos
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Nivel de confianza de la detección (0-1)",
        verbose_name="Confianza"
    )
    intensity = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Intensidad de la floración (0-100%)",
        verbose_name="Intensidad (%)"
    )
    
    # Datos adicionales
    notes = models.TextField(blank=True, verbose_name="Notas")
    photo = models.ImageField(upload_to='flowering/photos/', blank=True, verbose_name="Foto")
    
    # Usuario que registró (si aplica)
    reported_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Reportado por"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evento de floración"
        verbose_name_plural = "Eventos de floración"
        ordering = ['-detection_date']
    
    def __str__(self):
        return f"{self.plant_monitor.name} - {self.flowering_stage} ({self.detection_date.date()})"
