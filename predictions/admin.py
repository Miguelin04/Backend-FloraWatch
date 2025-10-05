"""
Configuración del admin para la aplicación Predictions
"""
from django.contrib import admin
from .models import (
    AIModel, PredictionSession, FloweringPrediction, 
    ModelPerformanceMetric, TrainingDataset
)


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'status', 'accuracy', 'created_by']
    list_filter = ['model_type', 'status', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    raw_id_fields = ['created_by']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PredictionSession)
class PredictionSessionAdmin(admin.ModelAdmin):
    list_display = ['session_type', 'model', 'start_date', 'end_date', 'status', 'total_predictions', 'executed_by']
    list_filter = ['session_type', 'status', 'model', 'created_at']
    search_fields = ['model__name']
    ordering = ['-created_at']
    raw_id_fields = ['model', 'executed_by']
    filter_horizontal = ['locations', 'plant_monitors']
    date_hierarchy = 'created_at'


@admin.register(FloweringPrediction)
class FloweringPredictionAdmin(admin.ModelAdmin):
    list_display = ['location', 'plant_monitor', 'prediction_type', 'target_date', 'flowering_probability', 'confidence_score']
    list_filter = ['prediction_type', 'prediction_date', 'target_date']
    search_fields = ['location__name', 'plant_monitor__name']
    ordering = ['-prediction_date', '-confidence_score']
    raw_id_fields = ['session', 'location', 'plant_monitor']
    date_hierarchy = 'prediction_date'


@admin.register(ModelPerformanceMetric)
class ModelPerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['model', 'metric_type', 'value', 'evaluation_date', 'dataset_size']
    list_filter = ['metric_type', 'evaluation_date']
    search_fields = ['model__name']
    ordering = ['-evaluation_date']
    raw_id_fields = ['model']
    date_hierarchy = 'evaluation_date'


@admin.register(TrainingDataset)
class TrainingDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'dataset_type', 'total_samples', 'quality_score', 'created_by']
    list_filter = ['dataset_type', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    raw_id_fields = ['created_by']
    readonly_fields = ['created_at', 'updated_at']
