# Generated by Django 3.2.20 on 2023-12-13 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchases', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderrequestitem',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.companybranch'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequestitem',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.company'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequestitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_order_items_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseorderrequestitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequestitem',
            name='stock_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.purchaseorderrequest'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequest',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.companybranch'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequest',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.company'),
        ),
        migrations.AddField(
            model_name='purchaseorderrequest',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_orders_createdby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseorderrequest',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.provider'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='branch',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.companybranch'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.company'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='product',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.product'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequestitem',
            name='stock_request',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchases.purchaseorderrequest'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequest',
            name='branch',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.companybranch'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequest',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.company'),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequest',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchaseorderrequest',
            name='provider',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user.provider'),
        ),
    ]