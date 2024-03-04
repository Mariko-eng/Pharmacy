# Create a file, e.g., templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='in_list')
def in_list(value, arg):
    # print(value)
    # print(arg)
    return value in arg.split(',')