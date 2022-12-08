# Generated by Django 4.1.4 on 2022-12-08 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_card_created_at_alter_card_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deadline',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
