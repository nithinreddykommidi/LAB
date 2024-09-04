# Generated by Django 4.1 on 2022-10-28 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2022, 10, 28, 16, 6, 54, 710727)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='group',
            field=models.CharField(blank=True, choices=[('O', 'O'), ('B', 'B'), ('AB', 'AB'), ('A', 'A')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='rh',
            field=models.CharField(blank=True, choices=[('-', '-'), ('+', '+')], max_length=20),
        ),
    ]