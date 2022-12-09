# Generated by Django 4.1.4 on 2022-12-09 02:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_card_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavourBoards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faves', to='api.board')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_faves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
