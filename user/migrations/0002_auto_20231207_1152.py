# Generated by Django 3.2.20 on 2023-12-07 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companydirector',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='companydirector',
            name='email',
        ),
        migrations.RemoveField(
            model_name='companydirector',
            name='name',
        ),
    ]
