# Generated by Django 5.1.1 on 2024-09-13 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0006_remove_order_created_at_alter_test_collection_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='HB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hb', models.CharField(blank=True, max_length=10)),
                ('hb_unit', models.CharField(blank=True, max_length=10)),
                ('hb_reference_range', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
