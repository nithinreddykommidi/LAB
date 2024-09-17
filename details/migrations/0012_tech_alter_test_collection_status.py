# Generated by Django 5.1.1 on 2024-09-16 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0011_alter_unitsandranges_hba1c_reference_range'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='test',
            name='collection_status',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=20),
        ),
    ]