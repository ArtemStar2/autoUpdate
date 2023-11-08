from django.urls import path
from .views import UserBalanceView, TransactionListView

urlpatterns = [
    path('', UserBalanceView.as_view(), name='user-balance'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
]