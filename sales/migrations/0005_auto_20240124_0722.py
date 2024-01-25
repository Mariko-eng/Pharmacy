# Generated by Django 3.2.20 on 2024-01-24 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20240124_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsaleitem',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
        migrations.AlterField(
            model_name='historicalsaleitem',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='historicalsaleitem',
            name='unit_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='quantity',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='unit_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]