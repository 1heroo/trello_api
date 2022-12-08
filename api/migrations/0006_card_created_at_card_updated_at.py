# Generated by Django 4.1.4 on 2022-12-08 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_board_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
