# Generated by Django 3.2.20 on 2024-01-30 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='uniqueId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
