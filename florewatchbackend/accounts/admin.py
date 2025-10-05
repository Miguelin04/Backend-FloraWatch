"""
Configuración del admin para la aplicación Accounts
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, APIKey, UserActivity, Notification


# Extender el admin de User para incluir UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'organization', 'contributions_count', 'predictions_made']
    list_filter = ['user_type', 'public_profile', 'email_notifications']
    search_fields = ['user__username', 'user__email', 'organization']
    ordering = ['user__username']
    raw_id_fields = ['user']


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'can_read', 'can_write', 'can_predict', 'is_active', 'usage_count']
    list_filter = ['can_read', 'can_write', 'can_predict', 'can_train', 'is_active']
    search_fields = ['user__username', 'name']
    ordering = ['-created_at']
    raw_id_fields = ['user']
    readonly_fields = ['key', 'usage_count', 'last_used']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'success', 'created_at']
    list_filter = ['activity_type', 'success', 'created_at']
    search_fields = ['user__username', 'description']
    ordering = ['-created_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'email_sent']
    search_fields = ['user__username', 'title', 'message']
    ordering = ['-created_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marcar como leídas"
