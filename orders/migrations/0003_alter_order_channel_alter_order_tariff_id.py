# Generated by Django 4.2.6 on 2023-11-04 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('service', '0001_initial'),
        ('orders', '0002_alter_order_channel_alter_order_tariff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='channel',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='orders', to='users.channel', verbose_name='Канал'),
        ),
        migrations.AlterField(
            model_name='order',
            name='tariff_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='service.tariff', verbose_name='Тариф'),
        ),
    ]
