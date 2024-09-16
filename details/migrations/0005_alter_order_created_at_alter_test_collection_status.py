# Generated by Django 5.1.1 on 2024-09-13 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0004_alter_order_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 9, 13, 23, 49, 40, 993018)),
        ),
        migrations.AlterField(
            model_name='test',
            name='collection_status',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=20),
        ),
    ]
