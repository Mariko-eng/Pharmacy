# Generated by Django 3.2.20 on 2024-01-04 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20240104_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]