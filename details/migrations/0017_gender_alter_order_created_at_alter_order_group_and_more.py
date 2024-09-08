# Generated by Django 4.2.15 on 2024-09-07 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0016_rename_required_date_locations_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required_date', models.DateField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 9, 7, 13, 44, 53, 7455)),
        ),
        migrations.AlterField(
            model_name='order',
            name='group',
            field=models.CharField(blank=True, choices=[('O', 'O'), ('B', 'B'), ('A', 'A'), ('AB', 'AB')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='rh',
            field=models.CharField(blank=True, choices=[('+', '+'), ('-', '-')], max_length=20),
        ),
        migrations.AlterField(
            model_name='test',
            name='collection_status',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=20),
        ),
    ]