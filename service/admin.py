from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Tariff, SocialNetwork

class ServiceAdmin(admin.ModelAdmin):
    def display_tariffs(self, obj):
        return ', '.join([str(tariff) for tariff in obj.tariffs.all()])
    
    list_display = ["id","name", "display_tariffs", "system_id"]
    search_fields = ["id", "name", "system_id"]

class TariffAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price_per_bot', 'price_per_minute')
    list_filter = ('price_per_bot', 'price_per_minute')
    search_fields = ('name',"price_per_bot", "price_per_minute")

class SocialNetworkAdmin(admin.ModelAdmin):
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет изображения"
    
    list_display = ["id","name", "display_image"]
    search_fields = ["id", "name"]
    
admin.site.register(Service, ServiceAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)