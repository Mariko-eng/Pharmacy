from django.db import models
from django.utils.translation import gettext as _

class DefaultRoles(models.TextChoices): 
    APP_ADMIN = 'App Admin', _('App Admin')
    ACCOUNT_HOLDER = 'Account Holder', _('Account Holder')
    COMPANY_ADMIN = 'Company Admin', _('Company Admin')
    STORE_MANAGER = 'Store Manager', _('Store Manager')
    INVENTORY_MANAGER = 'Inventory Manager',_('Inventory Manager')
    PROCUREMENT_OFFICER = 'Procurement Officer',_('Procurement Officer')
    SALES_MANAGER = 'Sales Manager',_('Sales Manager')
    FINANCE_MANAGER = 'Finance Manager',_('Finance Manager')
    CASHIER = 'Cashier', _('Cashier') 


APP_ADMIN_GROUP_ROLES = [
    DefaultRoles.APP_ADMIN,
]

COMPANY_ADMIN_GROUP_ROLES  = [
    DefaultRoles.ACCOUNT_HOLDER,
    DefaultRoles.COMPANY_ADMIN,
]

STORE_ADMIN_GROUP_ROLES  = [
    DefaultRoles.STORE_MANAGER,
    DefaultRoles.INVENTORY_MANAGER,
    DefaultRoles.PROCUREMENT_OFFICER,
    DefaultRoles.SALES_MANAGER,
    DefaultRoles.FINANCE_MANAGER,
]

POS_ATTENDANT_GROUP_ROLES  = [
    DefaultRoles.CASHIER,
]