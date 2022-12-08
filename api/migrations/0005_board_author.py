# Generated by Django 4.1.4 on 2022-12-08 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_board_image_delete_imageboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users_boards', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
