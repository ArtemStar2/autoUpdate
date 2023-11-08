from django.urls import path
from .views import OrderCreateView, PhraseListView, OrderListView,OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('phrases/', PhraseListView.as_view(), name='phrase-list'),
]