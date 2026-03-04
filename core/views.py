from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Booking, Service
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingSerializer,
    BookingUpdateSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    ServiceListSerializer,
    ServiceSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User registered successfully',
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful',
            }
        )


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password changed successfully'})


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logout successful'})
        except Exception:
            return Response({'message': 'Logout successful'})


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return ServiceListSerializer if self.action == 'list' else ServiceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        queryset = Service.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        if not request.user.is_admin:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            {
                'total_services': Service.objects.count(),
                'active_services': Service.objects.filter(is_active=True).count(),
            }
        )


class BookingViewSet(viewsets.ModelViewSet):
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
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            queryset = Booking.objects.all().select_related('user', 'service')
            status_filter = self.request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            return queryset
        return Booking.objects.filter(user=user).select_related('user', 'service')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user and not request.user.is_admin:
            return Response({'detail': 'You can only cancel your own bookings'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status in ['completed', 'cancelled']:
            return Response(
                {'detail': 'Cannot cancel a completed or already cancelled booking'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'booking cancelled'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        if user.is_admin:
            completed_with_price = Booking.objects.filter(status='completed').select_related('service')
            revenue = sum(b.service.price for b in completed_with_price)
            return Response(
                {
                    'total_bookings': Booking.objects.count(),
                    'pending_bookings': Booking.objects.filter(status='pending').count(),
                    'completed_bookings': Booking.objects.filter(status='completed').count(),
                    'cancelled_bookings': Booking.objects.filter(status='cancelled').count(),
                    'revenue': float(revenue),
                }
            )
        return Response(
            {
                'total_bookings': Booking.objects.filter(user=user).count(),
                'pending_bookings': Booking.objects.filter(user=user, status='pending').count(),
                'completed_bookings': Booking.objects.filter(user=user, status='completed').count(),
            }
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin(self, request):
        queryset = Booking.objects.all().select_related('user', 'service')
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        user_filter = request.query_params.get('user')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)
