# Generated by Django 3.2.20 on 2024-01-15 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_auto_20240110_0724'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0004_auto_20240111_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalproduct',
            old_name='updated_by_id',
            new_name='updated_by',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='updated_by_id',
            new_name='updated_by',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='available_qty',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='is_consummable',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='is_for_sale',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='item_photo',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='reorder_min_qty',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='store',
        ),
        migrations.RemoveField(
            model_name='historicalproduct',
            name='unit_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='available_qty',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_consummable',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_for_sale',
        ),
        migrations.RemoveField(
            model_name='product',
            name='item_photo',
        ),
        migrations.RemoveField(
            model_name='product',
            name='reorder_min_qty',
        ),
        migrations.RemoveField(
            model_name='product',
            name='store',
        ),
        migrations.RemoveField(
            model_name='product',
            name='unit_price',
        ),
        migrations.AlterField(
            model_name='historicalproductcategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalproductunits',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalproductvariant',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productunits',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='productunits',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('name', 'company')},
        ),
        migrations.CreateModel(
            name='StoreProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit_price', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('reorder_min_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('available_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('actual_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('is_consummable', models.BooleanField(default=False)),
                ('is_for_sale', models.BooleanField(default=True)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store_products_createdby', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalStoreProduct',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('unit_price', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('reorder_min_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('available_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('actual_qty', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('is_consummable', models.BooleanField(default=False)),
                ('is_for_sale', models.BooleanField(default=True)),
                ('updated_by', models.CharField(blank=True, max_length=225, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product')),
                ('store', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store')),
            ],
            options={
                'verbose_name': 'historical store product',
                'verbose_name_plural': 'historical store products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
