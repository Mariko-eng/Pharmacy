# Generated by Django 3.2.20 on 2024-01-24 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_auto_20240124_0727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalsale',
            old_name='sale_notes',
            new_name='sale_remarks',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='sale_notes',
            new_name='sale_remarks',
        ),
    ]