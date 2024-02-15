from company.models import Store
from company.models import StoreLevelGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from utils.groups.default_roles import DefaultRoles
from utils.permissions.user import user_app_specific_permissions


def init_store_groups(store_id=None):
    if store_id:
        store = Store.objects.get(pk = store_id)
        # Store Name
        store_name = store.name.replace(" ", "-")
        # Company Name
        company_name = store.company.name.replace(" ", "-")

        default_store_level_roles = [
            DefaultRoles.APP_ADMIN,
            DefaultRoles.ACCOUNT_HOLDER, 
            DefaultRoles.COMPANY_ADMIN, 
            DefaultRoles.STORE_MANAGER, 
            DefaultRoles.INVENTORY_MANAGER,
            DefaultRoles.PROCUREMENT_OFFICER, 
            DefaultRoles.SALES_MANAGER,
            DefaultRoles.FINANCE_MANAGER,
            DefaultRoles.CASHIER,
        ]

        for item in default_store_level_roles:
            # Role Name
            role_name = item.replace(" ", "-")
            # Group Name
            group_name = f"{company_name}_{store_name}_{role_name}"

            group, created = Group.objects.get_or_create(name=group_name)
            StoreLevelGroup.objects.get_or_create(store=store, group=group, name=role_name.replace("-", " "))

            all_permissions = Permission.objects.all()
            for codename, description in user_app_specific_permissions:
                user_app_permission, created = Permission.objects.get_or_create(codename=codename)

                for perm in all_permissions:
                    if user_app_permission != perm:
                        group.permissions.add(perm)


def create_store_group(role_name=None, store_id=None):
    if store_id and role_name:
        store = Store.objects.get(pk = store_id)
        # Store Name
        store_name = store.name.replace(" ", "-")
        # Company Name
        company_name = store.company.name.replace(" ", "-")
        # Role Name
        role_name = role_name.replace(" ", "-")

        # Group Name
        group_name = f"{company_name}_{store_name}_{role_name}"
        group, created = Group.objects.get_or_create(name=group_name)
        StoreLevelGroup.objects.get_or_create(store=store, group=group, name=role_name.replace("-", " "))
        return group
    else:
        return None