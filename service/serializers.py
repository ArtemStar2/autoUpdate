from rest_framework import serializers
from .models import Service, Tariff, SocialNetwork

class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = '__all__'

class ServiceTariffsSerializer(serializers.ModelSerializer):
    tariffs = TariffSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = "__all__"
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        
class SocialNetworkSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = SocialNetwork
        fields = "__all__"
        
