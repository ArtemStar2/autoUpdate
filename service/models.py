from django.db import models

# Соц сети
class SocialNetwork(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(upload_to='upload/', verbose_name="Логотип")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Социальные сети"
        verbose_name_plural = "Социальные сети"

# Сервисы
class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    social_networks = models.ForeignKey(SocialNetwork, related_name='services', on_delete=models.CASCADE, verbose_name="Социальная сеть")
    
    STATUS_CHOICES = [
        ('twitch', 'Twitch'),
        ('youtube', 'YouTube'),
        ('facebook', 'FaceBook'),
        ('wasd', 'WASD.TV'),
        ('trovo', 'Trovo'),
        ('tiktok', 'TikTok')
    ]

    type_service = models.CharField(choices=STATUS_CHOICES, verbose_name="Тип сервиса")
    
    system_id = models.IntegerField(default=0, verbose_name="Id накрутки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервисы"
        verbose_name_plural = "Сервисы"

# Тарифы
class Tariff(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    services = models.ManyToManyField(Service, related_name='tariffs', verbose_name="Сервис")
    
    # "цена за 1 бот" и "цена за 1 минуту"
    price_per_bot = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за 1 бот")
    price_per_minute = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за 1 минуту")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тарифы"
        verbose_name_plural = "Тарифы"