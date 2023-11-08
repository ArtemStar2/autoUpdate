from django.db import models
from django.contrib.auth.models import User

class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Баланс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"Баланс пользователя: {self.user.username}"
    
    class Meta:
        verbose_name = "Баланс пользователей"
        verbose_name_plural = "Баланс пользователей"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    transaction_type = models.CharField(max_length=100, verbose_name="Тип транзакции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    description = models.CharField(max_length=255, default="", null=True, verbose_name="Название платежа")
    
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('success', 'Успех'),
        ('error', 'Ошибка'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус платежа")

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.transaction_type}"
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"