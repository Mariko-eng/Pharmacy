from django.db import models
from django.utils.translation import gettext as _


class AccessGroups(models.TextChoices): # Access Group/ Account Type
    APP_ADMIN = 'App Admin', _('App Admin')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_ADMIN = 'Store Admin', _('Store Admin')
    POS_ATTENDANT = 'POS Attendant', _('POS Attendant')