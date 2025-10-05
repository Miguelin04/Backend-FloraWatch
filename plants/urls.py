"""
URLs para la aplicación Plants
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'species', views.PlantSpeciesViewSet, basename='species')
router.register(r'locations', views.LocationViewSet, basename='locations')
router.register(r'monitors', views.PlantMonitorViewSet, basename='monitors')
router.register(r'flowering-events', views.FloweringEventViewSet, basename='flowering-events')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints especiales
    path('species/<int:species_id>/flowering-calendar/', 
         views.FloweringCalendarView.as_view(), 
         name='flowering-calendar'),
    path('locations/<int:location_id>/current-flowering/', 
         views.CurrentFloweringView.as_view(), 
         name='current-flowering'),
    path('statistics/', 
         views.PlantStatisticsView.as_view(), 
         name='plant-statistics'),
]