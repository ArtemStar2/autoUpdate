from rest_framework import serializers

class BotsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'