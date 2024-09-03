# Generated by Django 4.1 on 2022-10-28 10:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_alter_patient_created_at_alter_patient_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='collected_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2022, 10, 28, 16, 9, 25, 608243)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='expected_complete_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='group',
            field=models.CharField(blank=True, choices=[('AB', 'AB'), ('B', 'B'), ('O', 'O'), ('A', 'A')], max_length=20),
        ),
    ]
