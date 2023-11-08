# Generated by Django 4.2.6 on 2023-11-04 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('system_id', models.IntegerField(default=0, verbose_name='Id накрутки')),
            ],
            options={
                'verbose_name': 'Сервисы',
                'verbose_name_plural': 'Сервисы',
            },
        ),
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
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price_per_bot', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за 1 бот')),
                ('price_per_minute', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за 1 минуту')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('services', models.ManyToManyField(related_name='tariffs', to='service.service', verbose_name='Сервис')),
            ],
            options={
                'verbose_name': 'Тарифы',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='social_networks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='service.socialnetwork', verbose_name='Социальная сеть'),
        ),
    ]
