from django.contrib import admin
from .models import UserBalance, Transaction

class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'balance', 'updated_at')  # Определите, какие поля отображать в списке
    list_filter = ('balance', 'updated_at')  # Добавьте фильтры по полям
    search_fields = ('user', 'balance', 'updated_at')  # Поле поиска
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id","user", "description", "amount", "transaction_type", "created_at", "status"]
    list_filter = ('user', 'amount', "transaction_type", "created_at", "status")
    search_fields = ["id", "user", "amount", "transaction_type", "status"]

admin.site.register(UserBalance, UserBalanceAdmin)
admin.site.register(Transaction, TransactionAdmin)