# Generated by Django 5.1 on 2024-09-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_is_synced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='qr_code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]