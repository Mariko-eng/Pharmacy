import random
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, AppRoles, CompanyRoles, BranchRoles

@receiver(post_save, sender = User)
def initailize_groups_after_creating_superuser(sender, instance, created, **kwargs):
    if created:
        # Code to run after the model instance is saved (created=True)
        print(f"{instance.email} has been created.")
        # Initialize Groups When creating the first super sueer
        if instance.is_superuser:
            # App Roles
            app_roles = AppRoles.choices
            for app_role in app_roles:
                group, created = Group.objects.get_or_create(name = app_role[0])
            # Company Roles
            company_roles = CompanyRoles.choices
            for company_role in company_roles:
                group, created = Group.objects.get_or_create(name = company_role[0])
            # Branch Roles
            branch_roles = BranchRoles.choices
            for branch_role in branch_roles:
                group, created = Group.objects.get_or_create(name = branch_role[0])
    else:
        # Code to run after the model instance is saved (created=False)
        print(f"{instance.email} has been updated.")


# Signal receiver function to generate a unique 6-digit number
@receiver(pre_save, sender = User)
def generate_unique_username(sender, instance, **kwargs):
    if not instance.username:
        # Generate a unique 6-digit number
        username = generate_6_digit_number(instance.first_name)

        while User.objects.filter(username=username).exists():
            # Keep generating a new unique number until it is truly unique
            username = generate_6_digit_number(instance.first_name)

        instance.username = username


def generate_6_digit_number(first_name):
    # Generate a random 6-digit number
    unique_no = '{:04}'.format(random.randint(0, 9999))
    return first_name + unique_no

