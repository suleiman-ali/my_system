from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    BookingViewSet,
    ChangePasswordView,
    LoginView,
    LogoutView,
    RegisterView,
    ServiceViewSet,
    UpdateProfileView,
    UserView,
)

service_router = DefaultRouter()
service_router.register(r'', ServiceViewSet, basename='service')

booking_router = DefaultRouter()
booking_router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('services/', include(service_router.urls)),
    path('bookings/', include(booking_router.urls)),
]
