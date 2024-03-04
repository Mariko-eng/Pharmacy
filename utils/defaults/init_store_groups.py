from company.models import Store
from company.models import StoreLevelGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from utils.groups.default_roles import DefaultRoles
from utils.permissions.user import app_admin_permissions
from utils.permissions.user import company_admin_permissions
from utils.permissions.user import store_manager_permissions
from utils.permissions.user import pos_attendant_permissions


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
        ]

        exluded_model_names = ['rolegroup', 'companyapplication', 'company', 'store']
        permissions_for_model = Permission.objects.filter(
            content_type__model__in=exluded_model_names
        )

        all_permissions_set = set(Permission.objects.all()) # Use a set insteead of a list
        app_and_company_admin_permissions = app_admin_permissions + company_admin_permissions
        # Get the permissions associated with the ContentType objects
        excluded_model_permissions_set = set(permissions_for_model)
 
        for item in default_store_level_roles:
            # Role Name
            role_name = item.replace(" ", "-") 
            # Group Name
            group_name = f"{company_name}_{store_name}_{role_name}"

            group, created = Group.objects.get_or_create(name=group_name)
            StoreLevelGroup.objects.get_or_create(store=store, group=group, name=role_name.replace("-", " "))

            # Create a set of non_store_permissions
            non_store_permissions_set = set()
            for codename, description in app_and_company_admin_permissions:
                permission = Permission.objects.get(codename=codename, name=description)
                non_store_permissions_set.add(permission) # Add items to the set

            # Add all other permissions to the group
            for perm in all_permissions_set - (non_store_permissions_set | excluded_model_permissions_set): # Subtract the sets
                group.permissions.add(perm)
            
            # Add specific store manager permissions
            for codename, description in store_manager_permissions:
                permission1 = Permission.objects.get(codename=codename, name=description)
                group.permissions.add(permission1)


        # Pos Attendant/Cashier Permissions
        # Role Name
        role_name = DefaultRoles.CASHIER.replace(" ", "-")
        group_name = f"{company_name}_{store_name}_{role_name}"              
        cashier_group, created = Group.objects.get_or_create(name=group_name)
        StoreLevelGroup.objects.get_or_create(store=store, group=cashier_group, name=role_name.replace("-", " "))
        for codename, description in pos_attendant_permissions:
            cashier_permission = Permission.objects.get(codename=codename, name=description)
            cashier_group.permissions.add(cashier_permission)



def create_store_group(store_id=None, role_name=None):
    try:
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
    except:
        return None