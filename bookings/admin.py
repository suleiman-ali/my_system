from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'preferred_date', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'service')
    search_fields = ('user__username', 'user__email', 'phone', 'address', 'problem_description')
    ordering = ('-created_at',)
    list_editable = ('status',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'service', 'problem_description', 'preferred_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Customer Info', {
            'fields': ('address', 'phone', 'payment_method')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Tarehe', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'service')
