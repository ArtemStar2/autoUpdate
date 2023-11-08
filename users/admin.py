from django.contrib import admin
from .models import Channel

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'url', 'channel_type', 'created_at','updated_at')  # Определите, какие поля отображать в списке
    list_filter = ('channel_type', 'user')  # Добавьте фильтры по полям
    search_fields = ('channel_type', 'user')  # Поле поиска
    
admin.site.register(Channel, ChannelAdmin)