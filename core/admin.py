from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Booking, Service, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'created_at')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2', 'is_admin')}),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'is_active')}),
        ('Tarehe', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'preferred_date', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'service')
    search_fields = ('user__username', 'user__email', 'phone', 'address', 'problem_description')
    ordering = ('-created_at',)
    list_editable = ('status',)
    fieldsets = (
        (None, {'fields': ('user', 'service', 'problem_description', 'preferred_date')}),
        ('Status', {'fields': ('status',)}),
        ('Customer Info', {'fields': ('address', 'phone', 'payment_method')}),
        ('Additional', {'fields': ('notes',)}),
        ('Tarehe', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'service')
