from django.contrib import admin
from .models import PhraseGroup, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'tariff_id', 'status', 'count_bots', 'count_minutes','created_at','updated_at')  # Определите, какие поля отображать в списке
    list_filter = ('count_bots', 'count_minutes', 'status')  # Добавьте фильтры по полям
    search_fields = ('user', 'tariff_id', 'count_bots', 'status','count_minutes')  # Поле поиска
    
class PhraseGroupAdmin(admin.ModelAdmin):
    list_display = ["id","user", "name"]
    search_fields = ["id", "user", "name"]

admin.site.register(Order, OrderAdmin)
admin.site.register(PhraseGroup, PhraseGroupAdmin)