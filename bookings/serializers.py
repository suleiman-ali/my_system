from rest_framework import serializers
from .models import Booking
from services.serializers import ServiceListSerializer


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'user_name', 'user_email', 'service', 'service_name', 
            'service_price', 'problem_description', 'preferred_date', 'status',
            'address', 'phone', 'payment_method', 'notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'status', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookingListSerializer(serializers.ModelSerializer):
    """Serializer for listing bookings (minimal info)"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = (
            'id', 'service_name', 'preferred_date', 'status', 
            'payment_method', 'created_at'
        )


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating bookings"""
    
    class Meta:
        model = Booking
        fields = (
            'service', 'problem_description', 'preferred_date',
            'address', 'phone', 'payment_method', 'notes'
        )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating booking status (admin only)"""
    
    class Meta:
        model = Booking
        fields = ('status', 'notes')
