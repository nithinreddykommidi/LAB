# Generated by Django 5.1.1 on 2024-10-07 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0023_alter_homevisit_status_alter_test_collection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homevisit',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
