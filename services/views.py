from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Service
from .serializers import ServiceSerializer, ServiceListSerializer


class IsAdminUser(permissions.BasePermission):
    """Permission to only allow admin users"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing services"""
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        queryset = Service.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get service statistics (admin only)"""
        if not request.user.is_admin:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        total_services = Service.objects.count()
        active_services = Service.objects.filter(is_active=True).count()
        
        return Response({
            'total_services': total_services,
            'active_services': active_services,
        })
