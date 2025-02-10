# Generated by Django 5.1.3 on 2024-12-11 00:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_products_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
