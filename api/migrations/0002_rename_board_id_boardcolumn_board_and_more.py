# Generated by Django 4.1.4 on 2022-12-08 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardcolumn',
            old_name='board_id',
            new_name='board',
        ),
        migrations.RenameField(
            model_name='boardcolumn',
            old_name='column_id',
            new_name='column',
        ),
        migrations.RenameField(
            model_name='boardmembers',
            old_name='board_id',
            new_name='board',
        ),
        migrations.RenameField(
            model_name='boardmembers',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='columncard',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='columncard',
            old_name='columns_id',
            new_name='columns',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='board_id',
            new_name='board',
        ),
        migrations.RenameField(
            model_name='markcard',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='markcard',
            old_name='mark_id',
            new_name='mark',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='members',
            old_name='user_id',
            new_name='user',
        ),
    ]
