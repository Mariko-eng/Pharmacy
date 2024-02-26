from company.models import Company
from company.models import CompanyLevelGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from utils.groups.default_roles import DefaultRoles
from utils.permissions.user import app_admin_permissions
from utils.permissions.user import superuser_permissions

from django.db.models import Count


def init_company_groups(company_id=None):
    if  company_id:
        company = Company.objects.get(pk = company_id)
        company_name = company.name.replace(" ", "-")

        default_company_level_roles = [
            DefaultRoles.APP_ADMIN,
            DefaultRoles.ACCOUNT_HOLDER, 
            DefaultRoles.COMPANY_ADMIN
        ]

        all_excluded_permissions = app_admin_permissions + superuser_permissions
    
        all_permissions_set = set(Permission.objects.all()) # Use a set insteead of a list
        all_excluded_permissions = [Permission.objects.get(
            codename=codename, name=description) for codename, description in all_excluded_permissions]
        # print("Here")
        all_excluded_permissions_set = set(all_excluded_permissions)

        for item in default_company_level_roles:
            role_name = item.replace(" ", "-")
            group_name = f"{company_name}_{role_name}"

            group, created = Group.objects.get_or_create(name=group_name)
            CompanyLevelGroup.objects.get_or_create(company=company, group=group, name=role_name.replace("-", " "))

            for perm in all_permissions_set - all_excluded_permissions_set:
                group.permissions.add(perm)


def create_company_group(company_id=None, role_name=None):
    try:
        if company_id and role_name:
            company = Company.objects.get(pk = company_id)
            company_name = company.name.replace(" ", "-")
            role_name = role_name.replace(" ", "-")
            group_name = f"{company_name}_{role_name}"
            group, created = Group.objects.get_or_create(name=group_name)
            CompanyLevelGroup.objects.get_or_create(company=company, group=group, name=role_name.replace("-", " "))
            return group
        else:
            return None
    except:
        return None
