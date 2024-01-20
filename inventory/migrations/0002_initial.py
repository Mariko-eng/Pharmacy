# Generated by Django 3.2.20 on 2024-01-20 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('company', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='storeproduct',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store_products_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product'),
        ),
        migrations.AddField(
            model_name='storeproduct',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='stockrequestitem',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='stockrequestitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_request_items_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockrequestitem',
            name='stock_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.stockrequest'),
        ),
        migrations.AddField(
            model_name='stockrequestitem',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='stockrequestitem',
            name='store_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.storeproduct'),
        ),
        migrations.AddField(
            model_name='stockrequest',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='stockrequest',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_requests_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stockrequest',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='receivedstockitem',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='receivedstockitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_stock_items_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='receivedstockitem',
            name='received_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.receivedstock'),
        ),
        migrations.AddField(
            model_name='receivedstockitem',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='receivedstockitem',
            name='store_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.storeproduct'),
        ),
        migrations.AddField(
            model_name='receivedstock',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='receivedstock',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_stocks_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='receivedstock',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='receivedstock',
            name='supplier_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.supplier'),
        ),
        migrations.AddField(
            model_name='receivedstock',
            name='supplier_store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_stock', to='company.store'),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='productunits',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='units',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.productunits'),
        ),
        migrations.AddField(
            model_name='product',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.productvariant'),
        ),
        migrations.AddField(
            model_name='outgoingconsumable',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company'),
        ),
        migrations.AddField(
            model_name='outgoingconsumable',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outgoing_consumables_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='outgoingconsumable',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.store'),
        ),
        migrations.AddField(
            model_name='outgoingconsumable',
            name='store_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.storeproduct'),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product'),
        ),
        migrations.AddField(
            model_name='historicalstoreproduct',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='stock_request',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.stockrequest'),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalstockrequestitem',
            name='store_product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.storeproduct'),
        ),
        migrations.AddField(
            model_name='historicalstockrequest',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalstockrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstockrequest',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalstockrequest',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='received_stock',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.receivedstock'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstockitem',
            name='store_product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.storeproduct'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='supplier_entity',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.supplier'),
        ),
        migrations.AddField(
            model_name='historicalreceivedstock',
            name='supplier_store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicalproductvariant',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalproductvariant',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproductunits',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalproductunits',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproductcategory',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalproductcategory',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.productcategory'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='units',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.productunits'),
        ),
        migrations.AddField(
            model_name='historicalproduct',
            name='variant',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.productvariant'),
        ),
        migrations.AddField(
            model_name='historicaloutgoingconsumable',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='historicaloutgoingconsumable',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaloutgoingconsumable',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaloutgoingconsumable',
            name='store',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.store'),
        ),
        migrations.AddField(
            model_name='historicaloutgoingconsumable',
            name='store_product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.storeproduct'),
        ),
        migrations.AlterUniqueTogether(
            name='productvariant',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='productunits',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'company')},
        ),
    ]
