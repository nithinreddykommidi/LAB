# Generated by Django 4.2.15 on 2024-08-18 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0006_alter_patient_collected_at_alter_patient_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='collection_status',
            field=models.ManyToManyField(blank=True, related_name='stat', to='details.test'),
        ),
        migrations.AddField(
            model_name='test',
            name='collection_status',
            field=models.CharField(blank=True, choices=[('no', 'no'), ('yes', 'yes')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='collected_at',
            field=models.CharField(choices=[('ATP', 'ATP'), ('KNR', 'KNR')], max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 8, 18, 13, 44, 34, 880427)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='group',
            field=models.CharField(blank=True, choices=[('B', 'B'), ('AB', 'AB'), ('O', 'O'), ('A', 'A')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='rh',
            field=models.CharField(blank=True, choices=[('-', '-'), ('+', '+')], max_length=20),
        ),
    ]