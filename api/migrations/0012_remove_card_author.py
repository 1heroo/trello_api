# Generated by Django 4.1.4 on 2022-12-08 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_card_column_delete_columncard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='author',
        ),
    ]