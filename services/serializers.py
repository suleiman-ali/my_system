from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model"""
    
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer for listing services (minimal info)"""
    
    class Meta:
        model = Service
        fields = ('id', 'name', 'price', 'is_active')
