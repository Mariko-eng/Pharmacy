# Generated by Django 3.2.20 on 2024-02-06 09:44

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSale',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('payment_option', models.CharField(choices=[('Cash', 'Cash'), ('Airtel MOney', 'Airtel MOney'), ('MTN MOney', 'MTN MOney'), ('Cheque', 'Cheque')], default='Cash', max_length=25)),
                ('payment_period', models.CharField(choices=[('Instant', 'Instant'), ('After 7 days', 'After 7 days'), ('After 14 days', 'After 14 days'), ('After 30 days', 'After 30 days'), ('After 60 days', 'After 60 days')], default='Instant', max_length=25)),
                ('payment_status', models.CharField(choices=[('PAID', 'PAID'), ('CURRENT', 'CURRENT'), ('OVERDUE', 'OVERDUE')], default='PAID', max_length=25)),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='Completed', max_length=25)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('invoice_file', models.TextField(max_length=100, null=True)),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical sale',
                'verbose_name_plural': 'historical sales',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSaleItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=12)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical sale item',
                'verbose_name_plural': 'historical sale items',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_option', models.CharField(choices=[('Cash', 'Cash'), ('Airtel MOney', 'Airtel MOney'), ('MTN MOney', 'MTN MOney'), ('Cheque', 'Cheque')], default='Cash', max_length=25)),
                ('payment_period', models.CharField(choices=[('Instant', 'Instant'), ('After 7 days', 'After 7 days'), ('After 14 days', 'After 14 days'), ('After 30 days', 'After 30 days'), ('After 60 days', 'After 60 days')], default='Instant', max_length=25)),
                ('payment_status', models.CharField(choices=[('PAID', 'PAID'), ('CURRENT', 'CURRENT'), ('OVERDUE', 'OVERDUE')], default='PAID', max_length=25)),
                ('status', models.CharField(choices=[('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='Completed', max_length=25)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('invoice_file', models.FileField(null=True, upload_to='invoices')),
                ('uniqueId', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=12)),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_paid', models.BooleanField(default=False)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
