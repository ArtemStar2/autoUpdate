from rest_framework import serializers
from .models import Order, PhraseGroup

class PhraseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhraseGroup
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'