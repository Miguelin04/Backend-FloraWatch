"""
Vistas para dashboards personalizados por tipo de usuario
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

from .models import UserProfile
from plants.models import FloweringEvent, PlantSpecies
from predictions.models import FloweringPrediction, AIModel


@login_required
def user_dashboard(request):
    """Dashboard principal que redirige según el tipo de usuario"""
    try:
        profile = request.user.userprofile
        user_type = profile.user_type
        
        if user_type == 'student':
            return redirect('student_dashboard')
        elif user_type == 'botanist':
            return redirect('botanist_dashboard')
        elif user_type == 'researcher':
            return redirect('researcher_dashboard')
        elif user_type == 'farmer':
            return redirect('farmer_dashboard')
        elif user_type == 'admin':
            return redirect('/admin/')
        else:
            return redirect('hobbyist_dashboard')
            
    except UserProfile.DoesNotExist:
        # Si no tiene perfil, crear uno básico
        UserProfile.objects.create(
            user=request.user,
            user_type='hobbyist'
        )
        return redirect('hobbyist_dashboard')


@login_required
def student_dashboard(request):
    """Dashboard para estudiantes"""
    profile = request.user.userprofile
    
    # Estadísticas para estudiantes
    context = {
        'user': request.user,
        'profile': profile,
        'total_predictions': FloweringPrediction.objects.count(),
        'total_species': PlantSpecies.objects.count(),
        'recent_events': FloweringEvent.objects.order_by('-detection_date')[:5],
        'dashboard_type': 'student'
    }
    
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
def botanist_dashboard(request):
    """Dashboard para botánicos"""
    profile = request.user.userprofile
    
    # Estadísticas para botánicos
    my_reports = FloweringEvent.objects.filter(reported_by=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'my_reports': my_reports.count(),
        'total_species': PlantSpecies.objects.count(),
        'recent_events': FloweringEvent.objects.order_by('-detection_date')[:10],
        'my_recent_reports': my_reports.order_by('-detection_date')[:5],
        'dashboard_type': 'botanist'
    }
    
    return render(request, 'accounts/botanist_dashboard.html', context)


@login_required
def researcher_dashboard(request):
    """Dashboard para investigadores"""
    profile = request.user.userprofile
    
    # Estadísticas para investigadores
    my_models = AIModel.objects.filter(created_by=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'my_models': my_models.count(),
        'active_models': AIModel.objects.filter(status='active').count(),
        'total_predictions': FloweringPrediction.objects.count(),
        'my_recent_models': my_models.order_by('-created_at')[:5],
        'dashboard_type': 'researcher'
    }
    
    return render(request, 'accounts/researcher_dashboard.html', context)


@login_required  
def farmer_dashboard(request):
    """Dashboard para agricultores"""
    profile = request.user.userprofile
    
    context = {
        'user': request.user,
        'profile': profile,
        'total_predictions': FloweringPrediction.objects.count(),
        'recent_predictions': FloweringPrediction.objects.order_by('-prediction_date')[:5],
        'dashboard_type': 'farmer'
    }
    
    return render(request, 'accounts/farmer_dashboard.html', context)


@login_required
def hobbyist_dashboard(request):
    """Dashboard para aficionados"""
    profile = request.user.userprofile
    
    context = {
        'user': request.user,
        'profile': profile,
        'total_species': PlantSpecies.objects.count(),
        'recent_events': FloweringEvent.objects.order_by('-detection_date')[:5],
        'dashboard_type': 'hobbyist'
    }
    
    return render(request, 'accounts/hobbyist_dashboard.html', context)


# API Views para login personalizado
@csrf_exempt
@api_view(['POST'])
def custom_login(request):
    """Login personalizado que redirige según el tipo de usuario"""
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username y password son requeridos'
        }, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user:
        if user.is_active:
            login(request, user)
            
            try:
                profile = user.userprofile
                dashboard_url = f'/dashboard/{profile.user_type}/'
            except UserProfile.DoesNotExist:
                dashboard_url = '/dashboard/hobbyist/'
            
            return Response({
                'success': True,
                'user_type': profile.user_type if hasattr(user, 'userprofile') else 'hobbyist',
                'dashboard_url': dashboard_url,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return Response({
                'error': 'Cuenta desactivada'
            }, status=401)
    else:
        return Response({
            'error': 'Credenciales inválidas'
        }, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_api(request):
    """API para obtener datos del dashboard del usuario"""
    
    try:
        profile = request.user.userprofile
        user_type = profile.user_type
        
        dashboard_data = {
            'user': {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'user_type': user_type
            },
            'profile': {
                'bio': profile.bio,
                'organization': profile.organization,
                'location': profile.location,
                'contributions_count': profile.contributions_count,
                'predictions_made': profile.predictions_made
            }
        }
        
        # Datos específicos por tipo de usuario
        if user_type == 'researcher':
            my_models = AIModel.objects.filter(created_by=request.user)
            dashboard_data['researcher_data'] = {
                'my_models_count': my_models.count(),
                'active_models': my_models.filter(status='active').count(),
                'recent_models': [
                    {
                        'name': model.name,
                        'status': model.status,
                        'accuracy': model.accuracy,
                        'created_at': model.created_at
                    } for model in my_models.order_by('-created_at')[:5]
                ]
            }
        
        elif user_type == 'botanist':
            my_reports = FloweringEvent.objects.filter(reported_by=request.user)
            dashboard_data['botanist_data'] = {
                'my_reports_count': my_reports.count(),
                'recent_reports': [
                    {
                        'plant': report.plant_monitor.name,
                        'stage': report.flowering_stage,
                        'date': report.detection_date
                    } for report in my_reports.order_by('-detection_date')[:5]
                ]
            }
        
        # Estadísticas generales
        dashboard_data['general_stats'] = {
            'total_species': PlantSpecies.objects.count(),
            'total_predictions': FloweringPrediction.objects.count(),
            'active_models': AIModel.objects.filter(status='active').count()
        }
        
        return Response(dashboard_data)
        
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Perfil de usuario no encontrado'
        }, status=404)