# Generated by Django 5.1.1 on 2024-10-20 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0027_remove_homevisit_date_homevisit_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='collection_status',
            field=models.CharField(choices=[('no', 'no'), ('yes', 'yes')], default='no', max_length=20),
        ),
    ]
