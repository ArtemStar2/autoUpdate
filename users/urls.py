from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, CurrentUserView, UserProfileUpdateView, ChannelListCreateView, ChannelUpdateView, ChangePasswordView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('info/', CurrentUserView.as_view(), name='info'),
    path('update/', UserProfileUpdateView.as_view(), name='update'),
    path('channels/', ChannelListCreateView.as_view(), name='channel-list-create'),
    path('channels/<int:pk>/', ChannelUpdateView.as_view(), name='channel-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]