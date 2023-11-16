# Generated by Django 3.2.23 on 2023-11-16 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='companybranch',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='companydirectors',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='companystaff',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='pos',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='posuser',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='user',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='company',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='companybranch',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='companydirectors',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='companystaff',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='pos',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='posuser',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='profile_pic'),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_by_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='companydirectors',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='companystaff',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pos',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='posuser',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posusers', to=settings.AUTH_USER_MODEL),
        ),
    ]
