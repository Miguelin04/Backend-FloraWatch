"""
URLs para la aplicación Satellite Data
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sources', views.SatelliteDataSourceViewSet, basename='sources')
router.register(r'collections', views.SatelliteDataCollectionViewSet, basename='collections')
router.register(r'data-points', views.SatelliteDataPointViewSet, basename='data-points')
router.register(r'weather', views.WeatherDataViewSet, basename='weather')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints especiales para datos satelitales
    path('ndvi/<int:location_id>/', 
         views.NDVIDataView.as_view(), 
         name='ndvi-data'),
    path('fetch-satellite-data/', 
         views.FetchSatelliteDataView.as_view(), 
         name='fetch-satellite-data'),
    path('locations/<int:location_id>/latest/', 
         views.LatestSatelliteDataView.as_view(), 
         name='latest-satellite-data'),
    path('batch-process/', 
         views.BatchProcessSatelliteDataView.as_view(), 
         name='batch-process'),
]