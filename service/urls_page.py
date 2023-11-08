from django.urls import path
from .views import custom_main_view, custom_service_view

urlpatterns = [
    path('', custom_main_view, name='main'),
    path('service/<int:service_id>/', custom_service_view, name='service'),
]