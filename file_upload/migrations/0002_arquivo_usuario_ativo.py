# Generated by Django 5.1.3 on 2024-11-08 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='usuario_ativo',
            field=models.CharField(choices=[('S', 'Sim'), ('N', 'Nao')], default='S', max_length=1),
        ),
    ]