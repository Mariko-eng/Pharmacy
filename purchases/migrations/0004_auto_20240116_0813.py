# Generated by Django 3.2.20 on 2024-01-16 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_auto_20240116_0721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpurchaseorderrequest',
            old_name='suppler_type',
            new_name='supplier_type',
        ),
        migrations.RenameField(
            model_name='purchaseorderrequest',
            old_name='suppler_type',
            new_name='supplier_type',
        ),
    ]
