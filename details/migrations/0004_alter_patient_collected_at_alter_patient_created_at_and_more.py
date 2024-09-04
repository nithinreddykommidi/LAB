# Generated by Django 4.1 on 2022-10-28 10:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0003_alter_patient_collected_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='collected_at',
            field=models.CharField(choices=[('KNR', 'KNR'), ('ATP', 'ATP')], max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2022, 10, 28, 16, 10, 10, 455726)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=50),
        ),
        migrations.AlterField(
            model_name='patient',
            name='group',
            field=models.CharField(blank=True, choices=[('AB', 'AB'), ('O', 'O'), ('A', 'A'), ('B', 'B')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='referred_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='details.doctor'),
        ),
    ]