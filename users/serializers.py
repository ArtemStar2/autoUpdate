from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import EmailValidator 
from .models import Channel

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator])
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'