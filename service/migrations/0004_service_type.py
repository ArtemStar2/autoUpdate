# Generated by Django 4.2.6 on 2023-11-08 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_socialnetwork_remove_tariff_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип сервиса'),
        ),
    ]