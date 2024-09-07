# Generated by Django 4.2.15 on 2024-09-07 10:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0013_locations_alter_customer_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='collected_at',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='details.locations'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 9, 7, 10, 46, 23, 24510)),
        ),
        migrations.AlterField(
            model_name='order',
            name='group',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('O', 'O'), ('AB', 'AB'), ('B', 'B')], max_length=20),
        ),
    ]
