from rest_framework import viewsets
from django.shortcuts import render
from .serializers import ServiceTariffsSerializer, SocialNetworkSerializer
from .models import Service, SocialNetwork,Tariff

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceTariffsSerializer
    
class SocialNetworkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialNetwork.objects.all()
    serializer_class = SocialNetworkSerializer
    
def custom_main_view(request):
    return render(request, 'main.html')

def custom_service_view(request, service_id):  
    services_and_tariffs = []

    # Получите все сервисы
    services = Service.objects.get(pk=service_id)

    # Теперь вы можете выполнить итерацию по сервисам и получить связанные тарифы для каждого сервиса
    service_data = {
        'service_type_service': services.type_service,
        'service_name': services.name,
        'tariffs': []
    }

    # Получите связанные тарифы для данного сервиса
    tariffs = Tariff.objects.filter(services=services)
    
    for tariff in tariffs:
        tariff_data = {
            'id' : tariff.id,
            'tariff_name': tariff.name,
            'description': tariff.description,
            'price_per_bot': float(tariff.price_per_bot),  # Преобразуйте Decimal в число
            'price_per_minute': float(tariff.price_per_minute),  # Преобразуйте Decimal в число
            'start_cost' : float(tariff.price_per_bot) + float(tariff.price_per_minute)
        }
        service_data['tariffs'].append(tariff_data)
        
    
    return render(request, 'service_list.html', {'service_data': service_data})