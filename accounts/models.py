"""
Modelos para la aplicación Accounts
Gestiona perfiles de usuario y autenticación
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserProfile(models.Model):
    """Perfil extendido para usuarios"""
    
    USER_TYPES = [
        ('researcher', 'Investigador'),
        ('student', 'Estudiante'),
        ('botanist', 'Botánico'),
        ('farmer', 'Agricultor'),
        ('hobbyist', 'Aficionado'),
        ('admin', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    user_type = models.CharField(max_length=20, choices=USER_TYPES, verbose_name="Tipo de usuario")
    
    # Información personal
    bio = models.TextField(blank=True, verbose_name="Biografía")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Organización")
    location = models.CharField(max_length=200, blank=True, verbose_name="Ubicación")
    
    # Información de contacto
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Número de teléfono inválido')],
        verbose_name="Teléfono"
    )
    website = models.URLField(blank=True, verbose_name="Sitio web")
    
    # Configuraciones
    email_notifications = models.BooleanField(default=True, verbose_name="Notificaciones email")
    public_profile = models.BooleanField(default=False, verbose_name="Perfil público")
    
    # Experiencia
    years_experience = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name="Años de experiencia"
    )
    specialization = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Especialización"
    )
    
    # Avatar
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name="Avatar"
    )
    
    # Estadísticas
    contributions_count = models.PositiveIntegerField(default=0, verbose_name="Contribuciones")
    predictions_made = models.PositiveIntegerField(default=0, verbose_name="Predicciones realizadas")
    accuracy_score = models.FloatField(
        null=True, 
        blank=True,
        verbose_name="Puntuación precisión"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(null=True, blank=True, verbose_name="Última actividad")
    
    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class APIKey(models.Model):
    """Claves API para usuarios"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    
    # Información de la clave
    name = models.CharField(max_length=100, verbose_name="Nombre descriptivo")
    key = models.CharField(max_length=64, unique=True, verbose_name="Clave")
    
    # Permisos
    can_read = models.BooleanField(default=True, verbose_name="Puede leer")
    can_write = models.BooleanField(default=False, verbose_name="Puede escribir")
    can_predict = models.BooleanField(default=True, verbose_name="Puede predecir")
    can_train = models.BooleanField(default=False, verbose_name="Puede entrenar")
    
    # Límites
    rate_limit_per_hour = models.PositiveIntegerField(
        default=1000, 
        verbose_name="Límite por hora"
    )
    rate_limit_per_day = models.PositiveIntegerField(
        default=10000, 
        verbose_name="Límite por día"
    )
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expira en")
    last_used = models.DateTimeField(null=True, blank=True, verbose_name="Último uso")
    
    # Estadísticas
    usage_count = models.PositiveIntegerField(default=0, verbose_name="Usos totales")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Clave API"
        verbose_name_plural = "Claves API"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class UserActivity(models.Model):
    """Registro de actividad de usuarios"""
    
    ACTIVITY_TYPES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('prediction', 'Predicción realizada'),
        ('model_training', 'Entrenamiento de modelo'),
        ('data_upload', 'Subida de datos'),
        ('api_call', 'Llamada API'),
        ('profile_update', 'Actualización perfil'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, verbose_name="Tipo")
    
    # Detalles de la actividad
    description = models.TextField(blank=True, verbose_name="Descripción")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Contexto adicional
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Metadatos"
    )
    
    # Resultado
    success = models.BooleanField(default=True, verbose_name="Exitoso")
    error_message = models.TextField(blank=True, verbose_name="Mensaje error")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Actividad de usuario"
        verbose_name_plural = "Actividades de usuario"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.created_at.date()})"


class Notification(models.Model):
    """Notificaciones para usuarios"""
    
    NOTIFICATION_TYPES = [
        ('prediction_ready', 'Predicción lista'),
        ('model_trained', 'Modelo entrenado'),
        ('flowering_detected', 'Floración detectada'),
        ('system_update', 'Actualización del sistema'),
        ('data_processed', 'Datos procesados'),
        ('error_alert', 'Alerta de error'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Baja'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, verbose_name="Tipo")
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='normal', verbose_name="Prioridad")
    
    # Contenido
    title = models.CharField(max_length=200, verbose_name="Título")
    message = models.TextField(verbose_name="Mensaje")
    
    # Enlaces
    action_url = models.URLField(blank=True, verbose_name="URL de acción")
    action_text = models.CharField(max_length=100, blank=True, verbose_name="Texto de acción")
    
    # Estado
    is_read = models.BooleanField(default=False, verbose_name="Leída")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Leída en")
    
    # Entrega
    email_sent = models.BooleanField(default=False, verbose_name="Email enviado")
    email_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Email enviado en")
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expira en")
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
