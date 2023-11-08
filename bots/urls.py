from django.urls import path
from .views import BotsView, BotsMessageView

urlpatterns = [
    path('', BotsView.as_view(), name='bots-all'),
    path('message/', BotsMessageView.as_view(), name='bots-message'),
]