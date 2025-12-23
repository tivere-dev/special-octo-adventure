from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationToken, PasswordResetToken, RefreshToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'email_verified', 'is_staff', 'date_joined', 'last_activity']
    list_filter = ['email_verified', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Email Verification', {'fields': ('email_verified', 'email_verified_at')}),
        ('Activity', {'fields': ('last_activity', 'remember_me')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'consumed', 'consumed_at']
    list_filter = ['consumed', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'consumed_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'consumed', 'consumed_at']
    list_filter = ['consumed', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'consumed_at']


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at', 'invalidated']
    list_filter = ['invalidated', 'created_at', 'expires_at']
    search_fields = ['user__email']
    readonly_fields = ['token', 'created_at', 'invalidated_at']
