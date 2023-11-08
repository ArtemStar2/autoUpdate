# Generated by Django 4.2.6 on 2023-11-08 01:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_remove_tariff_services_tariff_image_tariff_system_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(upload_to='upload/', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Социальные сети',
                'verbose_name_plural': 'Социальные сети',
            },
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='image',
        ),
        migrations.RemoveField(
            model_name='tariff',
            name='system_id',
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('system_id', models.IntegerField(default=0, verbose_name='Id накрутки')),
                ('social_networks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='service.socialnetwork', verbose_name='Социальная сеть')),
            ],
            options={
                'verbose_name': 'Сервисы',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.AddField(
            model_name='tariff',
            name='services',
            field=models.ManyToManyField(related_name='tariffs', to='service.service', verbose_name='Сервис'),
        ),
    ]