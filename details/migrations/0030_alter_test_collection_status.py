# Generated by Django 5.1.1 on 2024-10-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0029_alter_test_collection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='collection_status',
            field=models.CharField(choices=[('no', 'no'), ('yes', 'yes')], default='no', max_length=20),
        ),
    ]