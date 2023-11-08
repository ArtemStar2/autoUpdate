from django.db import models
from service.models import Tariff
from users.models import Channel
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Фразы
class PhraseGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название группы")
    phrases = models.TextField(verbose_name="Фразы")
       
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.phrases
    
    class Meta:
        verbose_name = "Фразы для чатов"
        verbose_name_plural = "Фразы для чатов"

# Заказы
class Order(models.Model):
    # Привязка к пользователям
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    # Привязка к тарифам
    tariff_id = models.ForeignKey(Tariff, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name="Тариф")
    # Привязка канала пользователя
    channel = models.ForeignKey(Channel, on_delete=models.SET_DEFAULT, null=True, default=None, related_name='orders', verbose_name="Канал")
    
    count_bots = models.IntegerField(verbose_name="Количество ботов", default=0)
    count_minutes = models.IntegerField(verbose_name="Количество минут", default=0)
    
    price = models.IntegerField(verbose_name="Стоимость", blank=True)
    login_bot = models.CharField(verbose_name="Логин бота", default=0,blank=True)
    
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('pause', 'Пауза'),
        ('success', 'Успех'),
        ('error', 'Ошибка'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус заказа")
    
    # Расширенные возможности
    auto_greeting = models.ForeignKey(PhraseGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='tariffs_auto_greeting', verbose_name="Автоматическое приветствие группа (группа фраз)")
    mass_message = models.ForeignKey(PhraseGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='tariffs_mass_message', verbose_name="Массовое сообщение (группа фраз)")
    interval_from = models.IntegerField(default=0, verbose_name="Интервал между сообщениями (От)")
    interval_to = models.IntegerField(default=1, verbose_name="Интервал между сообщениями (До)")
    bot_volume = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Объём охвата чат-ботов")
    
    # Настройка чат-ботов
    CHAT_BOT_MODE_CHOICES = [
        ('random', 'Случайно'),
        ('start', 'С начала'),
        ('end', 'С конца'),
    ]
    
    chat_bot_mode = models.CharField(max_length=10, choices=CHAT_BOT_MODE_CHOICES, default='random', verbose_name="Режим чата")
    send_interval_from = models.IntegerField(default=0, verbose_name="Интервал отправки (от)")
    send_interval_to = models.IntegerField(default=0, verbose_name="Интервал отправки (до)")
    dictionary = models.FileField(upload_to='upload/', blank=True, null=True, verbose_name="Словарь")
    auto_start_chat = models.BooleanField(default=False, verbose_name="Автозапуска чата")
    endless_messages = models.BooleanField(default=False, verbose_name="Бесконечные сообщения")
    
    # Настройка зрителей
    viewer_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Количество зрителей")
    auto_start_viewer = models.BooleanField(default=False, verbose_name="Активация автозапуска")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    
    def __str__(self):
        return f"Заказ пользователя: {self.user.username}"
    
    class Meta:
        verbose_name = "Заказы пользователей"
        verbose_name_plural = "Заказы пользователей"