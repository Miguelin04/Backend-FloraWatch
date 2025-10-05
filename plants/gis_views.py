"""
FloraWatch - Views Geoespaciales
APIs avanzadas para consultas espaciales con PostGIS
"""

from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceFilter, InBBoxFilter
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Location, PlantMonitor, FloweringEvent
from .serializers import LocationSerializer, PlantMonitorSerializer


class LocationGeoSerializer(GeoFeatureModelSerializer):
    """Serializer geoespacial para ubicaciones"""
    
    class Meta:
        model = Location
        geo_field = "coordinates"
        fields = (
            'id', 'name', 'coordinates', 'latitude', 'longitude',
            'altitude', 'country', 'region', 'description'
        )


class PlantMonitorGeoSerializer(GeoFeatureModelSerializer):
    """Serializer geoespacial para monitores de plantas"""
    
    location_coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = PlantMonitor
        geo_field = "location__coordinates"
        fields = (
            'id', 'name', 'species', 'location', 'location_coordinates',
            'installed_date', 'camera_type', 'status'
        )
    
    def get_location_coordinates(self, obj):
        if obj.location and obj.location.coordinates:
            return {
                'type': 'Point',
                'coordinates': [obj.location.coordinates.x, obj.location.coordinates.y]
            }
        return None


class LocationGeoViewSet(viewsets.ModelViewSet):
    """ViewSet con capacidades geoespaciales para ubicaciones"""
    
    queryset = Location.objects.all()
    serializer_class = LocationGeoSerializer
    filter_backends = [DistanceFilter, InBBoxFilter]
    distance_filter_field = 'coordinates'
    bbox_filter_field = 'coordinates'
    
    @action(detail=False, methods=['post'])
    def nearby(self, request):
        """Encontrar ubicaciones cercanas a un punto"""
        
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        radius_km = request.data.get('radius_km', 10)  # Default 10km
        
        if not lat or not lng:
            return Response({
                'error': 'Se requieren latitude y longitude'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            point = Point(float(lng), float(lat))
            
            # Buscar ubicaciones dentro del radio
            nearby_locations = Location.objects.filter(
                coordinates__distance_lte=(point, D(km=radius_km))
            ).annotate(
                distance=Distance('coordinates', point)
            ).order_by('distance')
            
            serializer = self.get_serializer(nearby_locations, many=True)
            
            return Response({
                'center_point': {'latitude': lat, 'longitude': lng},
                'radius_km': radius_km,
                'total_found': nearby_locations.count(),
                'locations': serializer.data
            })
            
        except (ValueError, TypeError) as e:
            return Response({
                'error': f'Coordenadas inválidas: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def in_region(self, request):
        """Encontrar ubicaciones dentro de una región (polígono)"""
        
        from django.contrib.gis.geos import Polygon
        
        coordinates = request.data.get('polygon_coordinates')
        
        if not coordinates:
            return Response({
                'error': 'Se requieren coordenadas del polígono'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Crear polígono desde coordenadas
            polygon = Polygon(coordinates)
            
            locations_in_region = Location.objects.filter(
                coordinates__within=polygon
            )
            
            serializer = self.get_serializer(locations_in_region, many=True)
            
            return Response({
                'polygon_area': polygon.area,
                'total_found': locations_in_region.count(),
                'locations': serializer.data
            })
            
        except Exception as e:
            return Response({
                'error': f'Polígono inválido: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def flowering_events_nearby(self, request, pk=None):
        """Eventos de floración cerca de esta ubicación"""
        
        location = self.get_object()
        radius_km = request.query_params.get('radius_km', 5)
        
        try:
            # Buscar eventos de floración cerca
            nearby_events = FloweringEvent.objects.filter(
                plant_monitor__location__coordinates__distance_lte=(
                    location.coordinates, D(km=float(radius_km))
                )
            ).select_related(
                'plant_monitor', 'plant_monitor__species', 'plant_monitor__location'
            ).order_by('-detection_date')
            
            events_data = []
            for event in nearby_events:
                distance = location.coordinates.distance(
                    event.plant_monitor.location.coordinates
                ) * 111  # Convertir a km aproximadamente
                
                events_data.append({
                    'id': event.id,
                    'plant_name': event.plant_monitor.name,
                    'species': event.plant_monitor.species.name,
                    'detection_date': event.detection_date,
                    'flowering_stage': event.flowering_stage,
                    'confidence_score': event.confidence_score,
                    'distance_km': round(distance, 2),
                    'location': {
                        'name': event.plant_monitor.location.name,
                        'coordinates': [
                            event.plant_monitor.location.coordinates.x,
                            event.plant_monitor.location.coordinates.y
                        ]
                    }
                })
            
            return Response({
                'location': location.name,
                'search_radius_km': radius_km,
                'total_events': len(events_data),
                'events': events_data
            })
            
        except Exception as e:
            return Response({
                'error': f'Error en búsqueda: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpatialAnalysisViewSet(viewsets.ViewSet):
    """ViewSet para análisis espaciales avanzados"""
    
    @action(detail=False, methods=['get'])
    def hotspots(self, request):
        """Identificar hotspots de floración"""
        
        from django.contrib.gis.db.models import Count
        from django.db.models import Q
        from datetime import datetime, timedelta
        
        # Parámetros
        days_back = int(request.query_params.get('days', 30))
        min_events = int(request.query_params.get('min_events', 3))
        
        # Fecha límite
        date_limit = datetime.now() - timedelta(days=days_back)
        
        # Agrupar eventos por ubicación
        hotspots = Location.objects.filter(
            plantmonitor__floweringevent__detection_date__gte=date_limit
        ).annotate(
            event_count=Count('plantmonitor__floweringevent')
        ).filter(
            event_count__gte=min_events
        ).order_by('-event_count')
        
        hotspot_data = []
        for location in hotspots:
            hotspot_data.append({
                'location_id': location.id,
                'name': location.name,
                'coordinates': [location.coordinates.x, location.coordinates.y],
                'event_count': location.event_count,
                'region': location.region,
                'country': location.country
            })
        
        return Response({
            'analysis_period_days': days_back,
            'minimum_events': min_events,
            'total_hotspots': len(hotspot_data),
            'hotspots': hotspot_data
        })
    
    @action(detail=False, methods=['post'])
    def density_map(self, request):
        """Crear mapa de densidad de especies o eventos"""
        
        # Implementar análisis de densidad usando PostGIS
        # ST_DWithin, ST_Buffer, etc.
        
        return Response({
            'message': 'Función de densidad en desarrollo',
            'available_soon': True
        })