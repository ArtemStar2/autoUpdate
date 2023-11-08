from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from balances.models import Transaction, UserBalance
from .models import Order, PhraseGroup
from .serializers import OrderSerializer, PhraseGroupSerializer
from service.models import Tariff
from users.models import Channel
from decimal import Decimal
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

import requests

class PhraseListView(generics.ListAPIView):
    queryset = PhraseGroup.objects.all()
    serializer_class = PhraseGroupSerializer

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.order_by('-created_at').filter(user=self.request.user)
    
class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id

        try:
            tariff = Tariff.objects.get(pk=request.data['tariff_id'])
        except Tariff.DoesNotExist:
            return Response({"detail": "Такого тарифа не существует"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            count_bots = Decimal(request.data['count_bots'])
        except:
            return Response({"detail": "Не ввидено количество ботов"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            count_minutes = Decimal(request.data['count_minutes'])
        except:
            return Response({"detail": "Не ввидено количество минут"}, status=status.HTTP_400_BAD_REQUEST)
        
        order_cost = (Decimal(tariff.price_per_bot) *count_bots) + (Decimal(tariff.price_per_minute) * count_minutes)
        
        if count_bots == 0 or count_minutes == 0:
            return Response({"detail": "Не ввидены количество ботов или минуты"}, status=status.HTTP_400_BAD_REQUEST)
        
        data["price"] = order_cost

        channel_id = request.data.get('channel')
        
        if not channel_id:
            return Response({"detail": "Не указан ID канала"}, status=status.HTTP_400_BAD_REQUEST)
        
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
        
        if not Channel.objects.filter(id=channel_id, user=user).exists():
            return Response({"detail": "Этот канал не принадлежит вам"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=data)           

        if serializer.is_valid() and order_cost:
            # user = request.user
            
            user_balance, created = UserBalance.objects.get_or_create(user=user)
            print(user_balance.balance)
            if user_balance.balance >= order_cost:
                try:
                    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
                    if response.status_code == 200:
                        response_data = response.json()
                        if response_data["userId"] != 0:
                            login_bot = response_data["userId"]
                        else:
                            return Response({"detail": "Ошибка сервиса"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "Ошибка сервиса"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"detail": "Не ввидено количество минут"}, status=status.HTTP_400_BAD_REQUEST)
                
                user_balance.balance -= order_cost
                user_balance.save()
                
                Transaction.objects.create(
                    user=user,
                    amount=order_cost,
                    transaction_type='debit',
                    description=tariff.name,
                    status='success'
                )
                
                order = serializer.save(user=user)
                order.login_bot = login_bot
                order.save()

                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Недостаточно средств"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)