# Generated by Django 4.1.4 on 2022-12-08 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_board_id_boardcolumn_board_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='board',
            name='image',
        ),
        migrations.AlterField(
            model_name='board',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='imageboard',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.board'),
        ),
    ]
