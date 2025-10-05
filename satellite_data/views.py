"""
Views para la aplicación Satellite Data
"""

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SatelliteDataSource, SatelliteDataCollection, SatelliteDataPoint, WeatherData
from .serializers import (
    SatelliteDataSourceSerializer, SatelliteDataCollectionSerializer,
    SatelliteDataPointSerializer, WeatherDataSerializer
)


class SatelliteDataSourceViewSet(viewsets.ModelViewSet):
    """ViewSet para fuentes de datos satelitales"""
    queryset = SatelliteDataSource.objects.all()
    serializer_class = SatelliteDataSourceSerializer


class SatelliteDataCollectionViewSet(viewsets.ModelViewSet):
    """ViewSet para colecciones de datos satelitales"""
    queryset = SatelliteDataCollection.objects.all()
    serializer_class = SatelliteDataCollectionSerializer


class SatelliteDataPointViewSet(viewsets.ModelViewSet):
    """ViewSet para puntos de datos satelitales"""
    queryset = SatelliteDataPoint.objects.all()
    serializer_class = SatelliteDataPointSerializer


class WeatherDataViewSet(viewsets.ModelViewSet):
    """ViewSet para datos meteorológicos"""
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer


class NDVIDataView(APIView):
    """Vista para datos NDVI"""
    
    def get(self, request, location_id):
        return Response({"message": "Datos NDVI - En desarrollo"})


class FetchSatelliteDataView(APIView):
    """Vista para obtener datos satelitales"""
    
    def post(self, request):
        return Response({"message": "Obtener datos satelitales - En desarrollo"})


class LatestSatelliteDataView(APIView):
    """Vista para últimos datos satelitales"""
    
    def get(self, request, location_id):
        return Response({"message": "Últimos datos satelitales - En desarrollo"})


class BatchProcessSatelliteDataView(APIView):
    """Vista para procesamiento en lote"""
    
    def post(self, request):
        return Response({"message": "Procesamiento en lote - En desarrollo"})
