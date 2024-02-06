import random
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import StockItem


# Signal receiver function to generate a unique 6-digit number
@receiver(pre_save, sender=StockItem)
def generate_unique_number(sender, instance, **kwargs):
    if not instance.unique_no:
        # Generate a unique 6-digit number
        unique_no = generate_6_digit_number()

        while StockItem.objects.filter(unique_no=unique_no).exists():
            # Keep generating a new unique number until it is truly unique
            unique_no = generate_6_digit_number()

        instance.unique_no = unique_no


def generate_6_digit_number():
    # Generate a random 6-digit number
    return '{:06}'.format(random.randint(0, 999999))
