# Generated by Django 4.1.4 on 2022-12-08 13:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_card_created_at_card_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
