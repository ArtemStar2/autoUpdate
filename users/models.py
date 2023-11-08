from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')
    url = models.CharField(max_length=100)

    STATUS_CHOICES = [
        ('twitch', 'Twitch'),
        ('youtube', 'YouTube'),
        ('facebook', 'FaceBook'),
        ('wasd', 'WASD.TV'),
        ('trovo', 'Trovo'),
        ('tiktok', 'TikTok')
    ]

    name_channel = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название канала")
    
    subscribers = models.IntegerField(default=0, verbose_name="Подписчиков")
    views = models.IntegerField(default=0, verbose_name="Просмотров")
    
    channel_type = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Тип канала")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    
    def __str__(self):
        return f"Канал пользователя: {self.user.username}"
    
    class Meta:
        verbose_name = "Каналы пользователей"
        verbose_name_plural = "Каналы пользователей"