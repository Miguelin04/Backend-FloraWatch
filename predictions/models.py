"""
Modelos para la aplicación Predictions
Gestiona predicciones de IA y análisis de floración
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from plants.models import PlantMonitor, Location
import json


class AIModel(models.Model):
    """Modelos de IA entrenados para predicciones"""
    
    MODEL_TYPES = [
        ('random_forest', 'Random Forest'),
        ('lstm', 'LSTM Neural Network'),
        ('cnn', 'Convolutional Neural Network'),
        ('ensemble', 'Ensemble Model'),
        ('isolation_forest', 'Isolation Forest (Anomalías)'),
    ]
    
    MODEL_STATUS = [
        ('training', 'Entrenando'),
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('deprecated', 'Obsoleto'),
        ('error', 'Error'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES, verbose_name="Tipo de modelo")
    version = models.CharField(max_length=20, verbose_name="Versión")
    description = models.TextField(verbose_name="Descripción")
    
    # Estado del modelo
    status = models.CharField(max_length=20, choices=MODEL_STATUS, default='training', verbose_name="Estado")
    accuracy = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Precisión"
    )
    
    # Configuración del modelo
    hyperparameters = models.JSONField(
        default=dict,
        blank=True,
        help_text="Hiperparámetros del modelo en JSON",
        verbose_name="Hiperparámetros"
    )
    
    # Archivos del modelo
    model_file_path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Ruta archivo modelo"
    )
    
    # Entrenamiento
    training_data_size = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Tamaño datos entrenamiento"
    )
    training_start_date = models.DateTimeField(null=True, blank=True, verbose_name="Inicio entrenamiento")
    training_end_date = models.DateTimeField(null=True, blank=True, verbose_name="Fin entrenamiento")
    
    # Usuario responsable
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Modelo de IA"
        verbose_name_plural = "Modelos de IA"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.model_type})"


class PredictionSession(models.Model):
    """Sesión de predicciones realizadas"""
    
    SESSION_TYPES = [
        ('flowering_detection', 'Detección de Floración'),
        ('flowering_prediction', 'Predicción de Floración'),
        ('anomaly_detection', 'Detección de Anomalías'),
        ('trend_analysis', 'Análisis de Tendencias'),
    ]
    
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, verbose_name="Modelo")
    session_type = models.CharField(max_length=50, choices=SESSION_TYPES, verbose_name="Tipo de sesión")
    
    # Configuración de la sesión
    start_date = models.DateField(verbose_name="Fecha inicio análisis")
    end_date = models.DateField(verbose_name="Fecha fin análisis")
    
    # Ubicaciones analizadas
    locations = models.ManyToManyField(
        Location,
        blank=True,
        verbose_name="Ubicaciones analizadas"
    )
    
    # Plantas específicas (opcional)
    plant_monitors = models.ManyToManyField(
        PlantMonitor,
        blank=True,
        verbose_name="Plantas específicas"
    )
    
    # Resultados de la sesión
    total_predictions = models.PositiveIntegerField(default=0, verbose_name="Total predicciones")
    successful_predictions = models.PositiveIntegerField(default=0, verbose_name="Predicciones exitosas")
    average_confidence = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Confianza promedio"
    )
    
    # Estado de la sesión
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pendiente'),
            ('running', 'Ejecutando'),
            ('completed', 'Completada'),
            ('error', 'Error'),
        ],
        default='pending',
        verbose_name="Estado"
    )
    
    # Usuario que ejecutó
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Ejecutado por")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completado en")
    
    class Meta:
        verbose_name = "Sesión de predicción"
        verbose_name_plural = "Sesiones de predicción"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.session_type} - {self.model.name} ({self.created_at.date()})"


class FloweringPrediction(models.Model):
    """Predicciones específicas de floración"""
    
    PREDICTION_TYPES = [
        ('detection', 'Detección actual'),
        ('forecast', 'Predicción futura'),
        ('anomaly', 'Detección de anomalía'),
    ]
    
    session = models.ForeignKey(
        PredictionSession, 
        on_delete=models.CASCADE, 
        related_name='predictions',
        verbose_name="Sesión"
    )
    
    # Ubicación y planta
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Ubicación")
    plant_monitor = models.ForeignKey(
        PlantMonitor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Planta específica"
    )
    
    # Predicción
    prediction_type = models.CharField(max_length=20, choices=PREDICTION_TYPES, verbose_name="Tipo")
    prediction_date = models.DateField(verbose_name="Fecha predicción")
    target_date = models.DateField(verbose_name="Fecha objetivo")
    
    # Resultados
    flowering_probability = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Probabilidad floración"
    )
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Confianza"
    )
    intensity_estimate = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Intensidad estimada (%)"
    )
    
    # Datos de entrada utilizados
    input_features = models.JSONField(
        default=dict,
        help_text="Características de entrada utilizadas para la predicción",
        verbose_name="Características entrada"
    )
    
    # Información adicional
    notes = models.TextField(blank=True, verbose_name="Notas")
    
    # Validación posterior
    actual_result = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name="Resultado real"
    )
    validation_date = models.DateField(null=True, blank=True, verbose_name="Fecha validación")
    validation_notes = models.TextField(blank=True, verbose_name="Notas validación")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Predicción de floración"
        verbose_name_plural = "Predicciones de floración"
        ordering = ['-prediction_date', '-confidence_score']
    
    def __str__(self):
        plant_name = self.plant_monitor.name if self.plant_monitor else "General"
        return f"{plant_name} - {self.prediction_date} (conf: {self.confidence_score:.2f})"


class ModelPerformanceMetric(models.Model):
    """Métricas de rendimiento de los modelos"""
    
    METRIC_TYPES = [
        ('accuracy', 'Precisión'),
        ('precision', 'Precisión (P)'),
        ('recall', 'Recall (R)'),
        ('f1_score', 'F1 Score'),
        ('mse', 'Error Cuadrático Medio'),
        ('mae', 'Error Absoluto Medio'),
        ('confusion_matrix', 'Matriz de Confusión'),
    ]
    
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, verbose_name="Modelo")
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES, verbose_name="Tipo métrica")
    
    # Valor de la métrica
    value = models.FloatField(verbose_name="Valor")
    
    # Contexto de evaluación
    evaluation_date = models.DateTimeField(verbose_name="Fecha evaluación")
    dataset_size = models.PositiveIntegerField(verbose_name="Tamaño dataset")
    dataset_description = models.TextField(blank=True, verbose_name="Descripción dataset")
    
    # Detalles adicionales
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Detalles adicionales de la métrica",
        verbose_name="Detalles"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Métrica de rendimiento"
        verbose_name_plural = "Métricas de rendimiento"
        ordering = ['-evaluation_date']
    
    def __str__(self):
        return f"{self.model.name} - {self.metric_type}: {self.value}"


class TrainingDataset(models.Model):
    """Datasets utilizados para entrenar modelos"""
    
    DATASET_TYPES = [
        ('phenocam', 'PhenoCam Network'),
        ('modis', 'MODIS Phenology'),
        ('inaturalist', 'iNaturalist'),
        ('synthetic', 'Datos Sintéticos'),
        ('user_contributed', 'Contribución Usuarios'),
        ('mixed', 'Dataset Mixto'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nombre")
    dataset_type = models.CharField(max_length=50, choices=DATASET_TYPES, verbose_name="Tipo dataset")
    description = models.TextField(verbose_name="Descripción")
    
    # Información del dataset
    total_samples = models.PositiveIntegerField(verbose_name="Total muestras")
    positive_samples = models.PositiveIntegerField(verbose_name="Muestras positivas")
    negative_samples = models.PositiveIntegerField(verbose_name="Muestras negativas")
    
    # Ubicación y fechas
    date_range_start = models.DateField(verbose_name="Inicio rango fechas")
    date_range_end = models.DateField(verbose_name="Fin rango fechas")
    
    # Archivos
    file_path = models.CharField(max_length=500, verbose_name="Ruta archivo")
    file_size_mb = models.FloatField(verbose_name="Tamaño archivo (MB)")
    
    # Calidad
    quality_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Puntuación calidad"
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Metadatos"
    )
    
    # Usuario responsable
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Creado por")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dataset de entrenamiento"
        verbose_name_plural = "Datasets de entrenamiento"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.total_samples} muestras)"
