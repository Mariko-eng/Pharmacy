# Generated by Django 3.2.20 on 2024-01-16 07:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20240116_0623'),
        ('purchases', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0015_auto_20240115_1559'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalSupplierEntity',
            new_name='HistoricalSupplier',
        ),
        migrations.RenameModel(
            old_name='SupplierEntity',
            new_name='Supplier',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='company',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='supplier_entity',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='supplier_store',
        ),
        migrations.AlterModelOptions(
            name='historicalsupplier',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical supplier', 'verbose_name_plural': 'historical suppliers'},
        ),
        migrations.DeleteModel(
            name='HistoricalProvider',
        ),
    ]
