from .models import UserBalance, Transaction
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .serializers import UserBalanceSerializer, TransactionSerializer
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        access_token = self.request.COOKIES.get('access')
        refresh_token = self.request.COOKIES.get('refresh')
        token = None
        try:
            token = AccessToken(access_token)
        except Exception as e:
            try:
                token = RefreshToken(refresh_token)               
            except Exception as e:
                token = None

        user = User.objects.get(id=token.payload.get('user_id'))
        # user = self.request.user
        return Transaction.objects.order_by('-created_at').filter(user=user)

class UserBalanceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # user = self.request.user
        access_token = self.request.COOKIES.get('access')
        refresh_token = self.request.COOKIES.get('refresh')
        token = None
        try:
            token = AccessToken(access_token)
        except Exception as e:
            try:
                token = RefreshToken(refresh_token)               
            except Exception as e:
                token = None

        user = User.objects.get(id=token.payload.get('user_id'))
        
        user_balance, created = UserBalance.objects.get_or_create(user=user)
        return user_balance

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        amount = Decimal(request.data.get('amount'))
        transaction_type = request.data.get('transaction_type')
        description = request.data.get('description')

        access_token = self.request.COOKIES.get('access')
        refresh_token = self.request.COOKIES.get('refresh')
        token = None
        try:
            token = AccessToken(access_token)
        except Exception as e:
            try:
                token = RefreshToken(refresh_token)               
            except Exception as e:
                token = None

        user = User.objects.get(id=token.payload.get('user_id'))
        
        if amount and transaction_type and description:
            if transaction_type == 'credit':
                instance.balance += amount
            elif transaction_type == 'debit':
                instance.balance -= amount

            instance.save()

            Transaction.objects.create(
                user=user,
                amount=amount,
                transaction_type=transaction_type,
                description=description
            )

            return self.retrieve(request, *args, **kwargs)

        return Response({"detail": "Неверные данные"}, status=status.HTTP_400_BAD_REQUEST)