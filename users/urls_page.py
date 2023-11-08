from django.urls import path
from .views import custom_register_view, custom_profile_view, custom_transactions_view, custom_channels_view, custom_orders_view, order_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', custom_register_view, name='register'),
    path('channels/', custom_channels_view, name='channels'),
    path('transactions/', custom_transactions_view, name='transactions'),
    path('orders/', custom_orders_view, name='orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('', custom_profile_view, name='info'),
]