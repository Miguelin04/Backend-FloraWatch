"""
Views para la aplicación Plants
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import PlantSpecies, Location, PlantMonitor, FloweringEvent
from .serializers import (
    PlantSpeciesSerializer, LocationSerializer, 
    PlantMonitorSerializer, FloweringEventSerializer
)


class PlantSpeciesViewSet(viewsets.ModelViewSet):
    """ViewSet para especies de plantas"""
    queryset = PlantSpecies.objects.all()
    serializer_class = PlantSpeciesSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet para ubicaciones"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class PlantMonitorViewSet(viewsets.ModelViewSet):
    """ViewSet para monitores de plantas"""
    queryset = PlantMonitor.objects.all()
    serializer_class = PlantMonitorSerializer


class FloweringEventViewSet(viewsets.ModelViewSet):
    """ViewSet para eventos de floración"""
    queryset = FloweringEvent.objects.all()
    serializer_class = FloweringEventSerializer


class FloweringCalendarView(APIView):
    """Vista para calendario de floración por especie"""
    
    def get(self, request, species_id):
        return Response({"message": "Calendario de floración - En desarrollo"})


class CurrentFloweringView(APIView):
    """Vista para floración actual por ubicación"""
    
    def get(self, request, location_id):
        return Response({"message": "Floración actual - En desarrollo"})


class PlantStatisticsView(APIView):
    """Vista para estadísticas de plantas"""
    
    def get(self, request):
        return Response({"message": "Estadísticas de plantas - En desarrollo"})
