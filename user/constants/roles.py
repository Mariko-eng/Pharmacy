from django.db import models
from django.utils.translation import gettext as _
# from .groups import UserTypes

class AccessLevels(models.TextChoices): # Access Levels
    APP_LEVEL = 'App Level', _('App Level')
    COMPANY_LEVEL = 'Company Level', _('Company Level')
    STORE_LEVEL = 'Store Level', _('Store Level')


class UserTypes(models.TextChoices): # Access Group/ Account Type
    # ROOT_ADMIN = 'Root Admin', _('Root Admin')
    APP_ADMIN = 'App Admin', _('App Admin')
    # ACCOUNT_HOLDER = 'Account Holder', _('Account Holder')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_ADMIN = 'Store Admin', _('Store Admin')
    POS_ATTENDANT = 'POS Attendant', _('POS Attendant')


class DefaultRoles(models.TextChoices): 
    ROOT_ADMIN = 'Root Admin', _('Root Admin')
    APP_ADMIN = 'App Admin', _('App Admin')
    ACCOUNT_HOLDER = 'Account Holder', _('Account Holder')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_ADMIN = 'Store Admin', _('Store Admin')
    POS_ATTENDANT = 'POS Attendant', _('POS Attendant')
    STORE_MANAGER = 'Store Manager', _('Store Manager')
    INVENTORY_MANAGER = 'Inventory Manager',_('Inventory Manager')
    PROCUREMENT_OFFICER = 'Procurement Officer',_('Procurement Officer')
    SALES_MANAGER = 'Sales Manager',_('Sales Manager')
    FINANCE_MANAGER = 'Finance Manager',_('Finance Manager')


APP_ACCESS_LEVEL_ROLES = [
    DefaultRoles.ROOT_ADMIN,
    DefaultRoles.APP_ADMIN,
]

COMPANY_ACCESS_LEVL_ROLES  = [
    DefaultRoles.ACCOUNT_HOLDER,
    DefaultRoles.COMPANY_ADMIN,
]

STORE_ACCESS_LEVEL_ROLES  = [
    DefaultRoles.STORE_ADMIN,
    DefaultRoles.POS_ATTENDANT,
    DefaultRoles.STORE_MANAGER,
    DefaultRoles.INVENTORY_MANAGER,
    DefaultRoles.PROCUREMENT_OFFICER,
    DefaultRoles.SALES_MANAGER,
    DefaultRoles.FINANCE_MANAGER,
]