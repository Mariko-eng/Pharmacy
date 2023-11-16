# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Permission
# from .models import Company

# @receiver(post_save, sender=Company)
# def create_permissions(sender, instance, created, **kwargs):
#     if created:
#         # Make sure the company is not None
#         if instance:
#             permissions = Permission.objects.all()

#             for permission in permissions:
#                 codename = f"{permission.name}_{instance.company.id}".lower()
#                 name = f"{permission.name} of company {instance.company.name} with Id {instance.company.id}".lower()

#                 # Using get_or_create to avoid duplicate permissions
#                 _, created_permission = Permission.objects.get_or_create(
#                     codename=codename,
#                     defaults={
#                         'name': name,
#                         'content_type': permission.content_type
#                     }
#                 )
