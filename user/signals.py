import random
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User
from .constants.roles import DefaultRoles

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        group, _ = Group.objects.get_or_create(name = DefaultRoles.ROOT_ADMIN)
        instance.groups.add(group)
        
 
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

