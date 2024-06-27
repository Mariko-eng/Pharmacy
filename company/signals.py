import random
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company, Store
from user.utils.init_company_groups import init_company_groups
from user.utils.init_store_groups import init_store_groups

@receiver(post_save, sender=Company)
def setup_company_groups_and_permissions(sender, instance, created, **kwargs):
    if created:
        init_company_groups(company_id=instance.pk)


@receiver(post_save, sender=Store)
def setup_store_groups_and_permissions(sender, instance, created, **kwargs):
    if created:
        init_store_groups(store_id=instance.pk)