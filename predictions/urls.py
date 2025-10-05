"""
URLs para la aplicación Predictions
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'models', views.AIModelViewSet, basename='models')
router.register(r'sessions', views.PredictionSessionViewSet, basename='sessions')
router.register(r'flowering-predictions', views.FloweringPredictionViewSet, basename='flowering-predictions')
router.register(r'performance-metrics', views.ModelPerformanceMetricViewSet, basename='performance-metrics')
router.register(r'training-datasets', views.TrainingDatasetViewSet, basename='training-datasets')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints para IA y predicciones
    path('predict/flowering/', 
         views.FloweringPredictionView.as_view(), 
         name='predict-flowering'),
    path('detect/current/', 
         views.CurrentFloweringDetectionView.as_view(), 
         name='detect-current'),
    path('train-model/', 
         views.TrainModelView.as_view(), 
         name='train-model'),
    path('model-status/<int:model_id>/', 
         views.ModelStatusView.as_view(), 
         name='model-status'),
    path('batch-predict/', 
         views.BatchPredictionView.as_view(), 
         name='batch-predict'),
    path('evaluate-model/<int:model_id>/', 
         views.EvaluateModelView.as_view(), 
         name='evaluate-model'),
]