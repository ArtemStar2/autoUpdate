from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from captcha.fields import ReCaptchaField
from django.contrib.auth import get_user_model
from googleapiclient.discovery import build

from balances.models import Transaction
from orders.models import Order
from .models import Channel
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserProfileUpdateSerializer, ChannelSerializer

import tldextract

def refresh_access_token(refresh_token):
    try:
        user = get_user_model().objects.get(id=refresh_token['user_id'])
        access_token = RefreshToken(refresh_token).access_token
        return access_token
    except Exception as e:
        # Обработайте ошибку, если не удается получить новый access-токен
        return None

api_key = "AIzaSyD_NweM1npZjVsgI9AoUzZCJSGZttOHlLg"
youtube_test = build('youtube', 'v3', developerKey=api_key)

def is_valid_social_media_url(url, channel_type):
    social_media_domains = [
        "twitch.tv",
        "youtube.com",
        "facebook.com",
        "wasd.tv",
        "trovo.live",
        "tiktok.com",
    ]

    extracted = tldextract.extract(url)
    domain = extracted.domain
    suffix = extracted.suffix

    if domain != channel_type:
        return False
    
    if f"{domain}.{suffix}" in social_media_domains:
        return True

    return False

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer  # Замените на ваш сериализатор
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@authentication_classes([])
@permission_classes([AllowAny])
class UserRegistrationView(APIView):
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError({'password': ['Пароль должен содержать не менее 8 символов.']})
        
    def post(self, request):
        data = request.data.copy()
        password = data['password']
        data['password'] = make_password(password)
        
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            if 'password' in data:
                try:
                    self.validate_password(password)
                except ValidationError as e:
                    return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'detail': "Пользователь успешно зарегистрирован",
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChannelUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
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

        return Channel.objects.filter(user=user)
    
    def perform_destroy(self, instance):
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
        
        if instance.user == user:
            instance.delete()
            return Response({"detail": "Запись успешно удалена."}, status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response({"detail": "У вас нет прав на удаление этой записи."}, status=status.HTTP_403_FORBIDDEN)
        
class ChannelListCreateView(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
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
        return self.queryset.filter(user=user)
        
    def post(self, request):
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get('refresh')
        # user = request.user
        token = None
        data = request.data.copy()
        try:
            token = AccessToken(access_token)
        except Exception as e:
            try:
                token = RefreshToken(refresh_token)               
            except Exception as e:
                token = None
        
        data['user'] = token.payload.get('user_id')
        if is_valid_social_media_url(request.data["url"], request.data["channel_type"]):
            
            if request.data["channel_type"] == "youtube":
                parts = request.data["url"].split("/")
                channel_id = parts[-1]

                if channel_id:
                    channel_info = youtube_test.channels().list(part='snippet,statistics', id=channel_id).execute()
                    channel_data = channel_info['items'][0]
                    channel_title = channel_data['snippet']['title']
                    subscribers_count = channel_data['statistics']['subscriberCount']
                    views_count = channel_data['statistics']['viewCount']

                    data["name_channel"] = channel_title
                    data["subscribers"] = subscribers_count
                    data["views"] = views_count
                else:
                    return Response({"detail": "Неверная ссылка на ютуб канал"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data["name_channel"] = request.data["channel_type"]
                data["subscribers"] = 0
                data["views"] = 0
                            
            serializer = ChannelSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Введена неверная ссылка"}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if new_password != confirm_new_password:
            return Response({"error": "Подтверждение нового пароля не совпадает"}, status=status.HTTP_400_BAD_REQUEST)

        form = PasswordChangeForm(request.user, request.data)

        if form.is_valid():
            form.save()
            return Response({"message": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
def custom_register_view(request):
    captcha = ReCaptchaField()
    return render(request, 'register.html', {'captcha' : captcha})

def custom_profile_view(request):
    return render(request, 'profile.html')

def custom_channels_view(request):
    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')

    try:
        token = AccessToken(access_token)
        user = User.objects.get(id=token.payload.get('user_id'))
        channels = Channel.objects.order_by('-created_at').filter(user=user)

    except Exception as e:
        try:
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token.payload.get('user_id'))
            channels = Channel.objects.order_by('-created_at').filter(user=user)

            access_token = str(token.access_token)
            
        except Exception as e:
            user = None
            channels = None
    
    if channels:
        for channel in channels:
            if channel.channel_type == "youtube":
                parts = channel.url.split("/")
                channel_id = parts[-1]

                if channel_id:
                    channel_info = youtube_test.channels().list(part='snippet,statistics', id=channel_id).execute()
                    channel_data = channel_info['items'][0]
                    subscribers_count = channel_data['statistics']['subscriberCount']
                    views_count = channel_data['statistics']['viewCount']

                    channel.subscribers = subscribers_count
                    channel.views = views_count

                    channel.save()
            else:
                channel.subscribers = 0
                channel.views = 0
    
    response = render(request, 'channels.html', {'channels': channels})
    response.set_cookie('access', access_token)
    response.set_cookie('refresh', refresh_token)
    return response

def custom_transactions_view(request):
    access_token = request.COOKIES.get('access')
    refresh_token = request.COOKIES.get('refresh')
    
    try:
        token = AccessToken(access_token)
        user = User.objects.get(id=token.payload.get('user_id'))
        transactions = Transaction.objects.order_by('-created_at').filter(user=user)

    except Exception as e:
        try:
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token.payload.get('user_id'))
            transactions = Transaction.objects.order_by('-created_at').filter(user=user)

            access_token = str(token.access_token)
            
        except Exception as e:
            user = None
            transactions = None
    
    response = render(request, 'transactions.html', {'transactions': transactions})
    response.set_cookie('access', access_token)
    response.set_cookie('refresh', refresh_token)
    return response

def custom_orders_view(request):
    refresh_token = request.COOKIES.get('refresh')
    access_token = request.COOKIES.get('access')

    try:
        token = AccessToken(access_token)
        user = User.objects.get(id=token.payload.get('user_id'))
        orders = Order.objects.order_by('-created_at').filter(user=user)

    except Exception as e:
        refresh_token = request.COOKIES.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            user = User.objects.get(id=token.payload.get('user_id'))
            orders = Order.objects.order_by('-created_at').filter(user=user)

            access_token = str(token.access_token)
            
            response = render(request, 'orders.html', {'orders': orders})
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)
            return response
        except Exception as e:
            orders = None
            
    response = render(request, 'orders.html', {'orders': orders})
    response.set_cookie('access', access_token)
    response.set_cookie('refresh', refresh_token)
    return response
    # return render(request, 'orders.html', {'orders': orders})

def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        return render(request, 'order_detail.html', {'order': order})
    except Order.DoesNotExist:
        return render(request, '404.html')