"""
Views para la aplicación Predictions
"""

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AIModel, PredictionSession, FloweringPrediction, ModelPerformanceMetric, TrainingDataset
from .serializers import (
    AIModelSerializer, PredictionSessionSerializer, FloweringPredictionSerializer,
    ModelPerformanceMetricSerializer, TrainingDatasetSerializer
)


class AIModelViewSet(viewsets.ModelViewSet):
    """ViewSet para modelos de IA"""
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer


class PredictionSessionViewSet(viewsets.ModelViewSet):
    """ViewSet para sesiones de predicción"""
    queryset = PredictionSession.objects.all()
    serializer_class = PredictionSessionSerializer


class FloweringPredictionViewSet(viewsets.ModelViewSet):
    """ViewSet para predicciones de floración"""
    queryset = FloweringPrediction.objects.all()
    serializer_class = FloweringPredictionSerializer


class ModelPerformanceMetricViewSet(viewsets.ModelViewSet):
    """ViewSet para métricas de rendimiento"""
    queryset = ModelPerformanceMetric.objects.all()
    serializer_class = ModelPerformanceMetricSerializer


class TrainingDatasetViewSet(viewsets.ModelViewSet):
    """ViewSet para datasets de entrenamiento"""
    queryset = TrainingDataset.objects.all()
    serializer_class = TrainingDatasetSerializer


class FloweringPredictionView(APIView):
    """Vista para predicciones de floración"""
    
    def post(self, request):
        return Response({"message": "Predicción de floración - En desarrollo"})


class CurrentFloweringDetectionView(APIView):
    """Vista para detección actual de floración"""
    
    def post(self, request):
        return Response({"message": "Detección actual - En desarrollo"})


class TrainModelView(APIView):
    """Vista para entrenar modelos"""
    
    def post(self, request):
        return Response({"message": "Entrenamiento de modelo - En desarrollo"})


class ModelStatusView(APIView):
    """Vista para estado del modelo"""
    
    def get(self, request, model_id):
        return Response({"message": "Estado del modelo - En desarrollo"})


class BatchPredictionView(APIView):
    """Vista para predicciones en lote"""
    
    def post(self, request):
        return Response({"message": "Predicciones en lote - En desarrollo"})


class EvaluateModelView(APIView):
    """Vista para evaluar modelo"""
    
    def post(self, request, model_id):
        return Response({"message": "Evaluación de modelo - En desarrollo"})
