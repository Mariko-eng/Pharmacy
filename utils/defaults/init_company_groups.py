from company.models import Company
from company.models import CompanyLevelGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from utils.groups.default_roles import DefaultRoles
from utils.permissions.user import user_company_admin_permissions


def init_company_groups(company_id=None):
    if  company_id:
        company = Company.objects.get(pk = company_id)
        company_name = company.name.replace(" ", "-")

        default_company_level_roles = [
            DefaultRoles.APP_ADMIN,
            DefaultRoles.ACCOUNT_HOLDER, 
            DefaultRoles.COMPANY_ADMIN
        ]

        for item in default_company_level_roles:
            role_name = item.replace(" ", "-")
            group_name = f"{company_name}_{role_name}"

            group, created = Group.objects.get_or_create(name=group_name)
            CompanyLevelGroup.objects.get_or_create(company=company, group=group, name=role_name.replace("-", " "))

            for codename, description in user_company_admin_permissions:
                user_company_permission, created = Permission.objects.get_or_create(codename=codename)
                group.permissions.add(user_company_permission)


def create_company_group(role_name=None, company_id=None):
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
