# Generated by Django 3.2.20 on 2024-01-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_auto_20240110_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsupplierentity',
            name='phone',
            field=models.CharField(max_length=225),
        ),
        migrations.AlterField(
            model_name='supplierentity',
            name='phone',
            field=models.CharField(max_length=225),
        ),
    ]