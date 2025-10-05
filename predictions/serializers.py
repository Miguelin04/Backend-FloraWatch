"""
Serializers para la aplicación Predictions
"""

from rest_framework import serializers
from .models import AIModel, PredictionSession, FloweringPrediction, ModelPerformanceMetric, TrainingDataset


class AIModelSerializer(serializers.ModelSerializer):
    """Serializer para modelos de IA"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = AIModel
        fields = '__all__'


class PredictionSessionSerializer(serializers.ModelSerializer):
    """Serializer para sesiones de predicción"""
    
    model_name = serializers.CharField(source='model.name', read_only=True)
    executed_by_username = serializers.CharField(source='executed_by.username', read_only=True)
    
    class Meta:
        model = PredictionSession
        fields = '__all__'


class FloweringPredictionSerializer(serializers.ModelSerializer):
    """Serializer para predicciones de floración"""
    
    location_name = serializers.CharField(source='location.name', read_only=True)
    plant_name = serializers.CharField(source='plant_monitor.name', read_only=True)
    
    class Meta:
        model = FloweringPrediction
        fields = '__all__'


class ModelPerformanceMetricSerializer(serializers.ModelSerializer):
    """Serializer para métricas de rendimiento"""
    
    model_name = serializers.CharField(source='model.name', read_only=True)
    
    class Meta:
        model = ModelPerformanceMetric
        fields = '__all__'


class TrainingDatasetSerializer(serializers.ModelSerializer):
    """Serializer para datasets de entrenamiento"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = TrainingDataset
        fields = '__all__'