# Generated by Django 4.1.4 on 2022-12-08 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_column_board_delete_boardcolumn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='markcard',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mark_cards', to='api.card'),
        ),
        migrations.AlterField(
            model_name='markcard',
            name='mark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_marks', to='api.mark'),
        ),
    ]