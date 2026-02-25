from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from .models import Booking
from .serializers import (
    BookingSerializer, 
    BookingListSerializer, 
    BookingCreateSerializer,
    BookingUpdateSerializer
)
from services.models import Service


class IsAdminUser(permissions.BasePermission):
    """Permission to only allow admin users"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing bookings"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        if self.action in ['update', 'partial_update']:
            if self.request.user.is_admin:
                return BookingUpdateSerializer
            return BookingSerializer
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # Users can only update their own bookings, admins can update any
            return [permissions.IsAuthenticated()]
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin sees all bookings
        if user.is_admin:
            queryset = Booking.objects.all().select_related('user', 'service')
            
            # Filter by status
            status_filter = self.request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            return queryset
        
        # Regular users see only their own bookings
        return Booking.objects.filter(user=user).select_related('user', 'service')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking (user can cancel their own)"""
        booking = self.get_object()
        
        if booking.user != request.user and not request.user.is_admin:
            return Response(
                {'detail': 'You can only cancel your own bookings'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status in ['completed', 'cancelled']:
            return Response(
                {'detail': 'Cannot cancel a completed or already cancelled booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'booking cancelled'})
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get booking statistics"""
        user = request.user
        
        if user.is_admin:
            # Admin sees all statistics
            total_bookings = Booking.objects.count()
            pending_bookings = Booking.objects.filter(status='pending').count()
            completed_bookings = Booking.objects.filter(status='completed').count()
            cancelled_bookings = Booking.objects.filter(status='cancelled').count()
            
            # Calculate revenue from completed bookings
            completed_with_price = Booking.objects.filter(
                status='completed'
            ).select_related('service')
            revenue = sum(b.service.price for b in completed_with_price)
            
            return Response({
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'completed_bookings': completed_bookings,
                'cancelled_bookings': cancelled_bookings,
                'revenue': float(revenue),
            })
        else:
            # Regular user sees their own statistics
            total_bookings = Booking.objects.filter(user=user).count()
            pending_bookings = Booking.objects.filter(user=user, status='pending').count()
            completed_bookings = Booking.objects.filter(user=user, status='completed').count()
            
            return Response({
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'completed_bookings': completed_bookings,
            })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin(self, request):
        """Get all bookings (admin only)"""
        queryset = Booking.objects.all().select_related('user', 'service')
        
        # Apply filters
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        user_filter = request.query_params.get('user')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)
