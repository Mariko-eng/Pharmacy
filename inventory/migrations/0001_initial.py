# Generated by Django 3.2.23 on 2023-12-03 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OutgoingConsumable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=12)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_no', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('item_photo', models.ImageField(null=True, upload_to='products')),
                ('unit_price', models.DecimalField(decimal_places=3, max_digits=12)),
                ('available_qty', models.DecimalField(decimal_places=3, max_digits=12)),
                ('reorder_min_qty', models.DecimalField(decimal_places=3, max_digits=12)),
                ('is_consummable', models.BooleanField(default=False)),
                ('is_for_sale', models.BooleanField(default=True)),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUnits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivered_by_name', models.CharField(max_length=255, unique=True)),
                ('delivered_by_phone', models.CharField(max_length=255, unique=True)),
                ('received_date', models.DateField(null=True)),
                ('delivery_notes', models.TextField(blank=True, null=True)),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedStockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(max_length=255, unique=True)),
                ('qty_received', models.DecimalField(decimal_places=3, max_digits=12)),
                ('unit_cost', models.DecimalField(decimal_places=3, max_digits=12)),
                ('manufactured_date', models.DateField(null=True)),
                ('expiry_date', models.DateField(null=True)),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined')], default='PENDING', max_length=10)),
                ('request_notes', models.TextField(blank=True, null=True)),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockRequestItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('updated_by_id', models.CharField(blank=True, max_length=225, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
